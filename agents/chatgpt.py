import openai
import os
from agents.agents import Agent


class ChatGPTAgent(Agent):

    def __init__(self, agent_name, model="gpt-4", self_checking:bool = False, **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.model = model
        self.conversation = []
        self.prompt_entity_initializer = "system"
        self.self_checking = self_checking
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def init_agent(self):
        if "Player 1" in self.role:
            self.update_conversation_tracking(self.prompt_entity_initializer, self.init_prompt())
            self.update_conversation_tracking("user", self.role)

        if "Player 2" in self.role:
            system_prompt = self.init_prompt() + self.role
            self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def chat(self):
        chat = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=0.7,
            max_tokens=600,
        )

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

    def make_trade(self):
        
        msg = super().make_trade()

        if self.self_checking:
            self.update_conversation_tracking("system", "Check your proposal to make sure you can win the game with this proposal. If you cannot, propose a new trade else propose the same trade.")
            msg = super().make_trade()
            
        return msg

