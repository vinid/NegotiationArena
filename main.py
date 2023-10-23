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

            self.check_exit_condition(trade_decision)
            
            # logic to update agent turn
            self.turn = 0 if self.turn == 1 else 1

    def check_exit_condition(self, decision):
        command = """{}. The proposal was accepted. I am the game master. Tell me the following:
        
                  MY RESOURCES: (these are your original resources)
                  ACCEPTED TRADE: (this is the trade that was accepted)
                  FINAL RESOURCES: (this is what you have after the trade) 
                  """

        if "ACCEPTED" in decision:

            agent_resources = []
            print('\n\n')

            init_res_sum = None
            final_res_sum = None
            
            for idx, agent in enumerate(self.agents):
                agent.update_conversation_tracking("user", command)
                resource = agent.chat().split("MY RESOURCES: ")[1]
                agent.update_conversation_tracking("assistant", resource)
                resource = Resources(text_to_dict(resource))
                agent_resources.append(resource)
                
                
                print("R{} INITIAL : ".format(idx), str(agent.inital_resources))
                print("R{} FINAL   : ".format(idx), str(resource))
                print("R{} GOAL    : ".format(idx), str(agent.goals))
                print("")

                if init_res_sum is None:
                    init_res_sum = agent.inital_resources
                else:
                    init_res_sum += agent.inital_resources
                
                if final_res_sum is None:
                    final_res_sum = resource
                else:
                    final_res_sum += resource
                
            if not final_res_sum.equal(init_res_sum):

                print("The sum of the resources is not the same as the original sum!")
                print("Original sum:", init_res_sum)
                print("Final sum:", final_res_sum)

            for idx, agent_res in enumerate(agent_resources):
                if self.agents[idx].goals.goal_reached(agent_res):
                    print("Agent {} REACHED the goal!".format(idx))
                else:
                    print("Agent {} DID NOT reach the goal!".format(idx))
            print("\n\n")

            for idx, agent in enumerate(self.agents):
                agent.dump_conversation("agent_{}.txt".format(idx))

            exit()


    def log(self):
        """
        Log conversation in human interpretable format
        """
        


potential_resources = ["X", "Y", "Z"]
potential_resources_txt = ",".join(potential_resources)

roles = {
    0: "You are Player 1, start by making an offer.", 
    1: "You are Player 2, start by responding to a trade."
}
n_rounds = 4

agent_init_resources = [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25, "Z": 30})]
agent_goals = [Goal({"X": 15, "Y": 15, "Z": 15}), Goal({"X": 15, "Y": 15, "Z": 15})]

agents = [ 
    ChatGPTAgent(model="gpt-4", 
                 potential_resources_txt=potential_resources_txt,
                 resources=init_res,
                 goals=goal,
                 role=roles[idx], 
                 n_rounds=n_rounds) 
               for idx, (init_res, goal) in enumerate(zip(agent_init_resources,agent_goals))
]

m = Manager(agents, n_rounds)
m.negotiate()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(m.agent1.conversation)


