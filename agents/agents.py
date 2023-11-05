from control.prompts import asking_for_final_results, TradingGame
from objects.utils import *
import copy
from objects.message import Message
from objects.utils import get_index_for_tag

class Agent:
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
        self.n_rounds = n_rounds
        self.potential_resources = potential_resources
        self.resources = [copy.deepcopy(resources)]
        self.agent_specific_messages_queue = []
        self.messages_history = []
        self.prompt_entity_initializer = None
        self.social_behaviour = social_behaviour

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
    
    def update_beliefs(self):
        
        # if no messages
        if not self.agent_specific_messages_queue:
            return
        
        # presently, assume only message
        msg = self.agent_specific_messages_queue.pop()

        # assume message is only about decision and/or proposal

        opponent_proposal = msg['proposed_trade']
        opponent_decision = msg['player_response']
        received_message = msg['message']


        player_response_str = f"<player response> {opponent_decision} </player response>"

        if type(opponent_proposal) == str:
            proposed_trade_str = f"<newly proposed trade> {opponent_proposal} </newly proposed trade>"
        else:
            proposed_trade_str = f"<newly proposed trade> {opponent_proposal.to_prompt()} </newly proposed trade>"
        message_str = f"<message>{received_message}</message>"

        opponent_response = ""
        for s, flag in zip([player_response_str, proposed_trade_str, message_str],
                           [opponent_decision, opponent_proposal, received_message]):
            if flag:
                opponent_response += (s  + "\n") 
        
        print('===========\n')
        # print("OPPONENT RESPONSE : \n{}".format(opponent_response))
        print("OPPONENT DECISION: \n {}".format(opponent_decision))
        print('===========\n')

        if opponent_response:
            self.update_conversation_tracking("user", opponent_response)

    def make_trade(self):
        # call agent / make agent think
        response = self.chat()

        # update agent history
        self.update_conversation_tracking("assistant", response)

        # parse the response
        my_resources, player_response, proposed_trade, message = parse_response(response)

        print(response)

        # send a message
        return Message({
            "proposed_trade": proposed_trade,
            "player_response": player_response,
            "message": message
        })

    def kill(self, decision):
        """
        Perform belief updates at end of agent life
        """
        # extract beliefs
        self.update_conversation_tracking("user", asking_for_final_results.format(decision))
        response = self.chat()

        # update conversation tracker
        self.update_conversation_tracking("assistant", response)

        start_index, end_index, tag_len = get_index_for_tag("final resources", response)
        final_resources = response[start_index + tag_len:end_index].strip()

        final_resources = Resources(text_to_dict(final_resources))
        self.resources.append(final_resources)

    def current_resources(self):
        return self.resources[-1]
        


