import os
from agents.agents import Agent
import time
import cohere

class CohereAgent(Agent):

    def __init__(self, agent_name, model="claude-2", **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.conversation = []
        self.model = model
        self.prompt_entity_initializer = "user"
        self.co = cohere.Client(os.environ.get("ANTHROPIC_API_KEY"))




    def chat(self):
        t = self.conversation_list_to_agent()

        completion = self.anthropic.completions.create(
            model=self.model,
            max_tokens_to_sample=400,
            prompt=t,
        )
        time.sleep(1)
        return completion.completion

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

