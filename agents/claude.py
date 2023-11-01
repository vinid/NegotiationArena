import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from agents.agents import Agent

class ClaudeAgent(Agent):

    def __init__(self, agent_name, **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.conversation = []
        self.prompt_entity_initializer = "user"
        self.anthropic = Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

    def conversation_list_to_agent(self):
        string = ""
        for o in self.conversation:
            t = o["content"]
            if o["role"] == "assistant":
                p = AI_PROMPT
            else:
                p = HUMAN_PROMPT
            string += f"{p} {t}"
        return f"{string} {AI_PROMPT}\n"

    def chat(self):
        t = self.conversation_list_to_agent()

        completion = self.anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=400,
            prompt=t,
        )
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

