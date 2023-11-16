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
    # TODO: entity or role?
    def update_conversation_tracking(self, entity, message):
        pass

    def init_agent(self, system_prompt):
        self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def receive_messages(self, message):    
        if message:
            self.update_conversation_tracking("user", message)

    def step(self, state):
        """
        Make agent take a step in a game:

        1. get state from game
        2. genereate a response to state
        3. return response

        """
        
        self.receive_messages(state.get('raw_response', None))            

        # call agent / make agent think
        response = self.chat()

        # update agent history
        self.update_conversation_tracking("assistant", response)

        return response

    def kill(self, decision_prompt):
        """
        Perform belief updates at end of agent life
        """

        self.update_conversation_tracking("user", decision_prompt)
        response = self.chat()

        # update conversation tracker
        self.update_conversation_tracking("assistant", response)

        return response

    def dump_conversation(self, file_name):
        pass

    def current_resources(self):
        return self.resources[-1]