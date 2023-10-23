from utils import *
import openai
import os
from prompts import *
from agents import *
import pprint
from dotenv import load_dotenv
from typing import List

load_dotenv('.env')

class Manager:

    def __init__(self, 
                 agents: List[ChatGPTAgent], 
                 n_rounds, 
                 model="gpt-4"
    ):  
        self.agents = agents
        self.agents_state = [dict() for _ in self.agents]
        self.n_rounds = n_rounds
        self.model = model
        
        # start with agent 0
        self.turn = 0

        for agent in self.agents:
            agent.update_conversation_tracking("system", agent.prompt())
        

    def negotiate(self):
        # negotiation over rounds
        for i in range(0, self.n_rounds*2):

            # check if other agent has proposal and/or decision
            # currently assume 2 agents
            if self.turn == 0:
                opponent_proposal = self.agents_state[1].get('proposed_trade', "")
                opponent_decision = self.agents_state[1].get('player_response', "")
            else:
                opponent_proposal = self.agents_state[0].get('proposed_trade', "")
                opponent_decision = self.agents_state[0].get('player_response', "")

            if i == 0:
                # there should be no existing proposals when game starts
                assert not (opponent_proposal or opponent_decision)

            opponent_response = opponent_decision + "\n" + opponent_proposal
            
            # append opponent response from previous iteration
            if opponent_response != "\n":
                self.agents[self.turn].update_conversation_tracking("user", opponent_response)

            # call agent
            response = self.agents[self.turn].chat()

            # parse the response
            trade_proposal, trade_decision, structured_state = parse_response(response)
            
            # TODO: Save a "timestamp/index" SOMEWHERE
            # update agent history
            self.agents[self.turn].update_conversation_tracking("assistant", response)
            # update agent state
            self.agents_state[self.turn] = {"player_response": trade_decision, "proposed_trade": trade_proposal }

            # debug
            print('\n=====')
            print("Iteration: {}".format(i))
            print("Turn: Player {}".format(self.turn))
            print("Player State: {}".format(structured_state))
            for k,v in self.agents_state[self.turn].items():
                print(k,":",v)
            
            print('=====')

            end = self.check_exit_condition(trade_decision)

            if end:
                return end
            
            # logic to update agent turn
            self.turn = 0 if self.turn == 1 else 1

        return "Game Over"

    def check_exit_condition(self, decision):
        command = """The proposal was accepted. I am the game master. Tell me the following:
        
                  MY RESOURCES: (these are your original resources)
                  ACCEPTED TRADE: (this is the trade that was accepted)
                  FINAL RESOURCES: (this is what you have after the trade) 
                  """

        if "ACCEPTED" in decision:

            agents_final_resources = []
            agents_initial_resources = []

            print('\n\n')

            init_res_sum = None
            final_res_sum = None
            
            for idx, agent in enumerate(self.agents):
                agent.update_conversation_tracking("user", command.format())

                response = agent.chat()

                original_resources = response.splitlines()[0].split("MY RESOURCES: ")[1]
                final_resources = response.splitlines()[2].split("FINAL RESOURCES: ")[1]

                #original_resources = Resources(text_to_dict(original_resources))
                final_resources = Resources(text_to_dict(final_resources))

                agents_final_resources.append(final_resources)
                agents_initial_resources.append(agent.inital_resources)

                print("R{} INITIAL : ".format(idx+1), str(agent.inital_resources))
                print("R{} FINAL   : ".format(idx+1), str(final_resources))
                print("R{} GOAL    : ".format(idx+1), str(agent.goals))
                print("")

                if init_res_sum is None:
                    init_res_sum = agent.inital_resources
                else:
                    init_res_sum += agent.inital_resources
                
                if final_res_sum is None:
                    final_res_sum = final_resources
                else:
                    final_res_sum += final_resources
                
            if not final_res_sum.equal(init_res_sum):

                print("The sum of the resources is not the same as the original sum!")
                print("Original sum:", init_res_sum)
                print("Final sum:", final_res_sum)

            results_of_negotiation = []
            for idx, agent_res in enumerate(agents_final_resources):
                if self.agents[idx].goals.goal_reached(agent_res):
                    print("Agent {} REACHED the goal!".format(idx))
                    results_of_negotiation.append(True)
                else:
                    print("Agent {} DID NOT reach the goal!".format(idx))
                    results_of_negotiation.append(False)
            print("\n\n")

            for idx, agent in enumerate(self.agents):
                agent.dump_conversation("agent_{}.txt".format(idx))

            scores = []
            for v1, v2 in zip(agents_final_resources, agents_initial_resources):
                s = v1 - v2
                scores.append(s.value())

            return final_res_sum.equal(init_res_sum), results_of_negotiation, scores

        else:
            return False

    def __exit__(self):
        for idx, agent in enumerate(self.agents):
            agent.dump_conversation("agent_{}.txt".format(idx))

    def log(self):
        """
        Log conversation in human interpretable format
        """
        

potential_resources = ["X", "Y"]
potential_resources_txt = ",".join(potential_resources)

roles = {
    0: "You are Player 1, start by making a proposal.", 
    1: "You are Player 2, start by responding to a trade."
}
n_rounds = 6

problem_sets = [
    [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    [Resources({"X": 25, "Y": 25}), Resources({"X": 10, "Y": 10})],
    [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],
]

all_things = []

for agent_init_resources in problem_sets:

    for i in range(5):

        agent_goals = [Goal({"X": 15, "Y": 15}), Goal({"X": 15, "Y": 15})]

        agents = [
            ChatGPTAgent(model="gpt-4",
                         potential_resources_txt=potential_resources_txt,
                         resources=init_res,
                         goals=goal,
                         role=roles[idx])
                       for idx, (init_res, goal) in enumerate(zip(agent_init_resources, agent_goals))
        ]

        m = Manager(agents, n_rounds)

        res = m.negotiate()

        if "Game Over" in res:
            all_things.append((False, None, None, None, None, str(agent_init_resources[0]),
                               str(agent_init_resources[1])))
        else:
            consistency, (winner_agent_1, winner_agent_2), (s1, s2) = res

            all_things.append((consistency, winner_agent_1, winner_agent_2, s1, s2, str(agent_init_resources[0]),
                           str(agent_init_resources[1])))

import csv

with open("final_dump.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["consistency", "winner_agent_1", "winner_agent_2", "s1", "s2", "agent_init_resources_0",
                     "agent_init_resources_1"])
    for row in all_things:
        writer.writerow(row)





