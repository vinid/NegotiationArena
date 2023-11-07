from control.prompts import prompt_for_final_results, TradingGame
from objects.utils import *
from abc import ABC, abstractmethod
import copy
from objects.message import Message
from objects.utils import get_index_for_tag

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

    @abstractmethod
    def chat(self):
        pass

    @abstractmethod
    def update_conversation_tracking(self, entity, message):
        pass

    def init_prompt(self):
        """
        Get initial system prompt for game setup.
        """
        
        return str(TradingGame(
            potential_resources=", ".join(self.potential_resources.available_items()),
            agent_initial_resources=self.resources[0].to_prompt(),
            agent_goal=self.goals.to_prompt(),
            n_rounds=self.n_rounds,
            agent_social_behaviour=self.social_behaviour))

    def init_agent(self):
        system_prompt = self.init_prompt() + self.role

        self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def receive_messages(self, msg):
        self.agent_specific_messages_queue.append(msg)
        self.update_beliefs()
    
    def update_beliefs(self):
        
        # if no messages
        if not self.agent_specific_messages_queue:
            return
        
        # presently, assume only message
        msg = self.agent_specific_messages_queue.pop()

        opponent_response = msg.to_opponent()
        
        if opponent_response:
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

    def kill(self, decision):
        """
        Perform belief updates at end of agent life
        """
        # extract beliefs

        self.update_conversation_tracking("user", prompt_for_final_results(decision))
        response = self.chat()

        # update conversation tracker
        self.update_conversation_tracking("assistant", response)

        print("FINAL RESPONSE: {}".format(response))

        start_index, end_index, tag_len = get_index_for_tag("final resources", response)
        final_resources = response[start_index + tag_len:end_index].strip()

        final_resources = Resources(text_to_dict(final_resources))
        self.resources.append(final_resources)

    def current_resources(self):
        return self.resources[-1]
        


