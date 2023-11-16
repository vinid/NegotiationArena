from abc import ABC
from game.agents.agents import Agent
from game.constants import REASONING_TAG

class SelfCheckingAgent(Agent, ABC):

    def think(self):
        
        # do one step of thinking
        super().think()
        print("reflecting!")
        # prompt agent to check proposal
        self.update_conversation_tracking("system", "Check your proposal to make sure you can win the game with this proposal. If you cannot, propose a new trade else propose the same trade.")
        # think again
        return super().think()
    
class ReasoningAgent(Agent, ABC):

    def think(self):
        print("reasonning!")
        
        # remind agent to think step by step
        self.update_conversation_tracking("system", f"Reason about your response step by step with <{REASONING_TAG}> [add reasoning] </{REASONING_TAG}>.")
        # think 
        return super().think()