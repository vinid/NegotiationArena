from abc import ABC, abstractmethod
import copy


class Agent(ABC):
    """
    Representing a Single LLM Agent
    """

    def __init__(self):

        self.model = None
        self.agent_name = None
        self.prompt_entity_initializer = None

    @abstractmethod
    def chat(self):
        pass

    @abstractmethod
    def update_conversation_tracking(self, entity, message):
        pass
    
    @abstractmethod
    def get_state(self,):
        """
        agent state refers to all information necessary to reproduce agent at a given time
        """
        pass

    # TODO: We don't use this for now
    # @abstractmethod
    def set_state(self):
        pass

    def init_agent(self, system_prompt):
        # clear conversation
        self.conversation = []
        self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def receive_messages(self, message):
        if message:
            self.update_conversation_tracking("user", message)

    def think(self):
        # call agent / make agent think
        response = self.chat()
    
        # update agent history
        self.update_conversation_tracking("assistant", response)

        return response 

    def step(self, state):
        """
        Make agent take a step in a game:

        1. get state from game
        2. genereate a response to state
        3. return response

        """
        self.receive_messages(state.get('raw_response', None))            

        response = self.think()

        return response