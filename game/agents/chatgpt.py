import copy
import openai
import os
from game.agents.agents import Agent
import time

class ChatGPTAgent(Agent):

    def __init__(self, agent_name, model="gpt-3.5-turbo", seed=None, **kwargs):

        super().__init__(**kwargs)
        self.run_epoch_time_ms = str(round(time.time() * 1000))
        self.agent_name = agent_name
        self.model = model
        self.conversation = []
        self.prompt_entity_initializer = "system"
        self.seed = int(self.run_epoch_time_ms) if seed is None else seed
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def init_agent(self, game_prompt):
        super().init_agent(str(game_prompt))


    def chat(self):
        chat = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=0.7,
            max_tokens=400,
            seed=self.seed
        )
        time.sleep(1)
        return chat["choices"][0]["message"]["content"]


    def get_state(self):
        return copy.deepcopy(self.__dict__)


    def update_conversation_tracking(self, role, message):
        # if same role, then append to existing message  
        if self.conversation and role == self.conversation[-1]['role']:
            last_msg = self.conversation[-1]
            new_msg = last_msg['content'] + "\n\n" + message
            last_msg['content'] = new_msg
            # self.conversation.append({"role": role, "content": message})
            return 
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
