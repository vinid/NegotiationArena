import os
from agents.agents import Agent
import time
import cohere

class LlamaAgent(Agent):

    def __init__(self, agent_name, **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.conversation = []


    def get_prompt_chat(message: str, chatbot: list[tuple[str, str]] = [],
                        system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
        input_prompt = f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n "
        for interaction in chatbot:
            input_prompt = input_prompt + str(interaction[0]) + " [/INST] " + str(interaction[1]) + " </s><s> [INST] "

        input_prompt = input_prompt + str(message) + " [/INST] "

        return input_prompt

    def init_agent(self, rulebook):

        if "Player 1" in self.role:
            # we use the user role to tell the assistant that it has to start.
            self.update_conversation_tracking(self.prompt_entity_initializer, self.init_prompt(rulebook))
            self.update_conversation_tracking("user", self.role)

        if "Player 2" in self.role:
            system_prompt = self.init_prompt(rulebook) + self.role
            self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def chat(self):

        pass

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

