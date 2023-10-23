from prompts import structured_calls
import openai
import os
from utils import Goal
import copy

class Agent:

    def __init__(self, potential_resources_txt, resources, goals: Goal, role):
        self.potential_resources_txt = potential_resources_txt
        self.inital_resources = copy.deepcopy(resources)
        self.resources = resources
        self.goals = goals
        self.role = role

    def prompt(self):
        return structured_calls.format(self.potential_resources_txt,
                                       self.resources.to_prompt(),
                                       self.goals.to_prompt(), self.role)

class ChatGPTAgent(Agent):

    def __init__(self, model="gpt4", **kwargs):
        super().__init__(**kwargs)
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
