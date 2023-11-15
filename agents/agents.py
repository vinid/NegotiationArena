from objects.utils import *
from abc import ABC, abstractmethod
import copy


class Agent(ABC):
    """
    Representing a Single Trading Agent
    """

    def __init__(self,
                 potential_resources,
                 resources,
                 goals: Goal,
                 n_rounds,
                 social_behaviour,
                 role):

        self.role = role
        self.goals = goals
        self.model = None
        self.n_rounds = n_rounds
        self.potential_resources = potential_resources
        self.resources = [copy.deepcopy(resources)]
        self.agent_specific_messages_queue = []
        self.messages_history = []
        self.prompt_entity_initializer = None
        self.social_behaviour = social_behaviour
        self.agent_name = None


    @abstractmethod
    def chat(self):
        pass

    @abstractmethod
    def update_conversation_tracking(self, entity, message):
        pass

    def init_prompt(self, rulebook):
        """
        Get initial system prompt for game setup.
        """
        
        return str(rulebook.instantiate_initial_prompt(
            self.potential_resources,
            self.resources[0],
            self.goals,
            self.n_rounds,
            self.social_behaviour
        ))

    def init_agent(self, rulebook):
        system_prompt = self.init_prompt(rulebook) + self.role

        self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def receive_messages(self, msg):

        opponent_response = msg.to_opponent()
        
        self.update_conversation_tracking("user", opponent_response)

    def think_next_action(self):
        # call agent / make agent think
        response = self.chat()

        print('\n================')
        print(response)
        print('================\n')

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

    
    def inject_conversation_history(self, conversation_history):
        """
        
        """
        pass
        

class SelfCheckingAgent(Agent, ABC):

    def think_next_action(self):
        
        # do one step of thinking
        msg = super().think_next_action()
        # add prompt to check proposal
        print('Agent checking proposal...')
        self.update_conversation_tracking("system", "Check your proposal to make sure you can win the game with this proposal. If you cannot, propose a new trade else propose the same trade.")
        # think
        return super().think_next_action()
            

                   