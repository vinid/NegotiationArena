from prompts import structured_calls, asking_for_final_results
import openai
import os
from utils import *
import copy

class Agent:
    """
    Representing a Single Trading Agent
    """

    def __init__(self, 
                 potential_resources,
                 resources, 
                 goals: Goal,
                 n_rounds, 
                 role):
        self.role = role
        self.goals = goals
        self.n_rounds = n_rounds
        self.potential_resources = potential_resources
        self.resources = [copy.deepcopy(resources)]
        self.agent_specific_messages_queue = []
        self.messages_history = []

        # for now, define marginal utility as proportional to distance to objective
        self.marginal_utility = goals-self.resources[0]

    def init_prompt(self):
        return structured_calls.format(", ".join(self.potential_resources.available_items()),
                                       self.resources[0].to_prompt(),
                                       self.goals.to_prompt(), 
                                       self.n_rounds,
                                       self.role,
                                       )
    def init_agent(self):
        self.update_conversation_tracking("system", self.init_prompt())

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
        message = msg['message']

        if opponent_decision:       
            opponent_response = "PLAYER RESPONSE : {}".format(opponent_decision) + "\n" + \
                                "PROPOSED TRADE : {}".format(opponent_proposal.to_prompt()) + "\n" + \
                                "MESSAGE : {}".format(message)
        else:
            opponent_response = "PROPOSED TRADE : {}".format(opponent_proposal.to_prompt()) + "\n" + \
                                "MESSAGE : {}".format(message)

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
        self.update_conversation_tracking("system", asking_for_final_results.format(decision))
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
        


class ChatGPTAgent(Agent):

    def __init__(self, agent_name, model="gpt4",  **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.model = model
        self.conversation = []
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def chat(self):
        chat = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=0.7,
            max_tokens=400,
        )

        return chat["choices"][0]["message"]["content"]

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})

    def dump_conversation(self, file_name):
        with open(file_name, "w") as f:
            for index, text in enumerate(self.conversation):
                c = text["content"].replace("\n", " ")
                
                if index % 2 == 0:
                    f.write(f"= = = = = Iteration {index//2} = = = = =\n\n")
                    f.write(f'{text["role"]}: {c}' "\n\n")
                else:
                    f.write(f'\t\t{text["role"]}: {c}' "\n\n")
