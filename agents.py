from prompts import structured_calls
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
                 role):
        self.role = role
        self.goals = goals
        self.potential_resources = potential_resources
        # list enables use to index resources over time
        self.resources = [copy.deepcopy(resources)]
        self.messages_queue = []
        self.messages_history = []
        

        # for now, define marginal utility as proportional to distance to objective
        self.marginal_utility = goals-resources[0]

    def init_prompt(self):
        return structured_calls.format(", ".join(self.potential_resources.available_items()),
                                       self.resources[0].to_prompt(),
                                       self.goals.to_prompt(), 
                                       self.role)
    def init_agent(self):
        self.update_conversation_tracking("system", self.init_prompt())


    def receive_messages(self, msg):
        self.messages_queue.append(msg)
    
    def update_beliefs(self):
        
        # if no messages
        if not self.messages:
            return
        
        # presently, assume only message
        msg = self.messages_queue[-1]

        # assume message is only about decision and/or proposal
        opponent_proposal = msg['trade_proposal']
        opponent_decision = msg['trade_decision']  
        
        if opponent_decision:       
            opponent_response = "PLAYER RESPONSE : {}".format(opponent_decision) + "\n" + \
                            "PROPOSED TRADE : {}".format(opponent_proposal.to_prompt())
        else:
            opponent_response = "PROPOSED TRADE : {}".format(opponent_proposal.to_prompt())

        self.agents[self.turn].update_conversation_tracking("user", opponent_response)

    def make_trade(self):
        # call agent / make agent think
        response = self.agents[self.turn].chat()

        # update agent history
        self.agents[self.turn].update_conversation_tracking("assistant", response)

        # parse the response
        structured_state = parse_response(response)

        # send a message
        return Message({
            "trade_proposal" : structured_state.trade_proposal
        })


        
        # if opponent_proposal:
        # structured_state["in_trade_utility"] = opponent_proposal.utility(self.agents[0].marginal_utility, self.agents[1].marginal_utility)
        # structured_state["marginal_utility"] = [agent.marginal_utility for agent in self.agents]
        # if "proposed_trade" in structured_state:
        # structured_state["out_trade_utility"] = structured_state['proposed_trade'].utility(self.agents[0].marginal_utility, self.agents[1].marginal_utility)
            


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
            temperature=0, 
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
