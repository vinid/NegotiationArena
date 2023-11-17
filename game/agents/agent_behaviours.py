from abc import ABC
from game.agents.agents import Agent
from game.constants import REASONING_TAG

class SelfCheckingAgent(Agent, ABC):

    def think(self):
        # do one step of thinking
        super().think()
        # print("reflecting!")
        # prompt agent to check proposal
        self.update_conversation_tracking("user", "Check your proposal to make sure you can win the game with this proposal. If you cannot, propose a new trade else propose the same trade.")
        # think again
        return super().think()
    
class ReasoningAgent(Agent, ABC):

    def init_agent(self, system_prompt):
        system_prompt = system_prompt + f"Reason succinctly step by step about your response within <{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> tags."
        super().init_agent(system_prompt)
        

    # def think(self):
    #     # print("reasoning!")
    #     # remind agent to think step by step
    #     # self.update_conversation_tracking("user", f"Reason succinctly step by step about your response within <{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> tags.")
    #     # think 
    #     return super().think()