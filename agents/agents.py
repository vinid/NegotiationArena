from control.prompts import structured_calls, asking_for_final_results
from objects.utils import *
import copy
from objects.message import Message

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

        # for now, define marginal utility as proportional to distance to objective
        self.marginal_utility = goals-self.resources[0]

    def init_prompt(self):
        return structured_calls.format(", ".join(self.potential_resources.available_items()),
                                       self.resources[0].to_prompt(),
                                       self.goals.to_prompt(), 
                                       self.n_rounds, self.social_behaviour
                                       )
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


        player_response_str = "PLAYER RESPONSE : {}".format(opponent_decision)
        proposed_trade_str = "PROPOSED TRADE : {}".format(opponent_proposal.to_prompt())
        message_str = "MESSAGE : {}".format(received_message)

        opponent_response = ""
        for s, flag in zip([player_response_str, proposed_trade_str, message_str],
                           [opponent_decision, opponent_proposal, received_message]):
            if flag:
                opponent_response += (s  + "\n") 
        print("OPPONENT RESPONSE : {}".format(opponent_response))
        if opponent_response:
            self.update_conversation_tracking("user", opponent_response)

    def make_trade(self):
        # call agent / make agent think
        response = self.chat()

        # update agent history
        self.update_conversation_tracking("assistant", response)

        # parse the response
        my_resources, player_response, proposed_trade, message = parse_response(response)

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

        # parse response
        response_lines = [ _ for _ in response.splitlines() if _.strip('\n')]

        # extract final resources
        final_resources = response_lines[2].split("FINAL RESOURCES: ")[1]
        final_resources = Resources(text_to_dict(final_resources))
        self.resources.append(final_resources)

    def current_resources(self):
        return self.resources[-1]
        


