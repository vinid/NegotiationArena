import openai
import os
from game.agents.agents import Agent
import time

class ChatGPTAgent(Agent):

    def __init__(self, agent_name, model="gpt-3.5-turbo", **kwargs):

        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.model = model
        self.conversation = []
        self.prompt_entity_initializer = "system"
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def init_agent(self, game_prompt):
        self.update_conversation_tracking(self.prompt_entity_initializer, str(game_prompt))

    def chat(self):
        chat = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=0.2,
            max_tokens=400,
        )
        time.sleep(1)
        return chat["choices"][0]["message"]["content"]

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})

    def dump_conversation(self, file_name):
        with open(file_name, "w") as f:
            for index, text in enumerate(self.conversation):
                c = text["content"].replace("\n", " ")

                if index % 2 == 0:
                    f.write(f"= = = = = Iteration {index // 2} = = = = =\n\n")
                    f.write(f'{text["role"]}: {c}' "\n\n")
                else:
                    f.write(f'\t\t{text["role"]}: {c}' "\n\n")
