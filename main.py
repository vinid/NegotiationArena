from utils import *
import openai
import os
from prompts import *
from agents import *
import pprint



potential_resources = ["X", "Y", "Z"]
potential_resources_txt = ",".join(potential_resources)

roles = {1: "You are Player 1, start by proposing a trade.", 2: "You are Player 2, start by responding to a trade."}
n_rounds = 10

agent_1_initial_resources = Resources({"X": 25, "Y": 15})
agent_2_initial_resources = Resources({"X": 5, "Y": 25, "Z": 30})

agent1 = ChatGPTAgent(model="gpt-4", potential_resources_txt=potential_resources_txt,
               resources=agent_1_initial_resources,
               goals=Goal({"X": 15, "Y": 15, "Z": 15}),
               role=roles[1])

agent2 = ChatGPTAgent(model="gpt-4", potential_resources_txt=potential_resources_txt,
               resources=agent_2_initial_resources,
               goals=Goal({"X": 15, "Y": 15, "Z": 15}),
               role=roles[2])


class Manager:

    def __init__(self, agent1: ChatGPTAgent, agent2 : ChatGPTAgent, n_rounds, model="gpt-4"):
        self.agent1 = agent1
        self.agent2 = agent2
        self.n_rounds = n_rounds
        self.model = model

        self.agent1.update_conversation_tracking("system", agent1.prompt())
        self.agent2.update_conversation_tracking("system", agent2.prompt())

    def negotiate(self):
        # negotiation over rounds
        for i in range(1, self.n_rounds + 1):

            # we ask the first agent
            response = self.agent1.chat()

            # we parse the response
            trade_proposal, trade_decision, structured_state = parse_response(response)

            # updating both conversations
            self.agent1.update_conversation_tracking("assistant", response)

            self.check_exit_condition(trade_decision)

            if i != 1:
                trade_proposal = trade_decision + "\n" + trade_proposal

            self.agent2.update_conversation_tracking("user", trade_proposal)

            response2 = self.agent2.chat()

            trade_proposal2, trade_decision2, structured_state2 = parse_response(response2)

            if "ACCEPTED" not in trade_decision2:
                trade_proposal = trade_decision2 + "\n" + trade_proposal2

            # updating both conversations
            self.agent1.update_conversation_tracking("user", trade_proposal)
            self.agent2.update_conversation_tracking("assistant", response2)

            self.check_exit_condition(trade_decision2)

    def check_exit_condition(self, decision):
        command = """{}. The proposal was accepted. I am the game master. Tell me the following:
        
                  MY RESOURCES: (these are your original resources)
                  ACCEPTED TRADE: (this is the trade that was accepted)
                  FINAL RESOURCES: (this is what you have after the trade) 
                  """

        if "ACCEPTED" in decision:
            self.agent1.update_conversation_tracking("user", command.format("Hello, Player 1"))
            self.agent2.update_conversation_tracking("user", command.format("Hello, Player 2"))
            resources_agent1 = self.agent1.chat()
            resources_agent2 = self.agent2.chat()
            self.agent1.update_conversation_tracking("assistant", resources_agent1)
            self.agent2.update_conversation_tracking("assistant", resources_agent2)

            resources_agent1 = resources_agent1.split("FINAL RESOURCES: ")[1]
            resources_agent2 = resources_agent2.split("FINAL RESOURCES: ")[1]
            print()
            print()
            print("R1:", resources_agent1)
            print("R2:", resources_agent2)

            final_res_1 = Resources(text_to_dict(resources_agent1))
            final_res_2 = Resources(text_to_dict(resources_agent2))

            final_sum = final_res_2 + final_res_1
            original_sum = agent_1_initial_resources + agent_2_initial_resources

            if not final_sum.equal(original_sum):
                print("The sum of the resources is not the same as the original sum!")
                print("Original sum:", original_sum)
                print("Final sum:", final_sum)

            if self.agent1.goals.goal_reached(final_res_1):
                print("Agent 1 reached the goal!")
            else:
                print("Agent 1 did not reach the goal!")
            if self.agent2.goals.goal_reached(final_res_2):
                print("Agent 2 reached the goal!")
            else:
                print("Agent 2 did not reach the goal!")

            self.agent1.dump_conversation("agent1.txt")
            self.agent2.dump_conversation("agent2.txt")

            exit()

    def __exit__(self):
        self.agent1.dump_conversation("agent1.txt")
        self.agent2.dump_conversation("agent2.txt")





m = Manager(agent1, agent2, n_rounds)
m.negotiate()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(m.agent1.conversation)


