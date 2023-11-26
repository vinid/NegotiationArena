import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from ratbench.agents.agents import Agent
import time
from copy import copy, deepcopy
from ratbench.constants import AGENT_TWO, AGENT_ONE


class ClaudeAgent(Agent):

    def __init__(self, agent_name, model="claude-2.1", use_system_prompt=True, **kwargs):
        super().__init__(**kwargs)
        self.run_epoch_time_ms = str(round(time.time() * 1000))

        self.agent_name = agent_name
        self.conversation = []
        self.model = model
        self.use_system_prompt = use_system_prompt
        self.role_to_prompt = {
            "user": HUMAN_PROMPT,
            "assistant": AI_PROMPT,
        }
        self.prompt_entity_initializer = "system"
        self.anthropic = Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

    def init_agent(self, system_prompt, role):

        if AGENT_ONE in self.agent_name:
            # we use the user role to tell the assistant that it has to start.
            self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)
            self.update_conversation_tracking("user", role)

        elif AGENT_TWO in self.agent_name:
            system_prompt = system_prompt + role
            self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)
        else:
            raise "No Player 1 or Player 2 in role"

        # system_prompt = system_prompt + role
        # self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():

            if (type(v)) == Anthropic:
                v = "AnthropicObject"
            setattr(result, k, deepcopy(v, memo))
        return result

    def messages_to_prompt(self, messages):
        prompt = ""

        # if we use the claude2.1 system prompt style. we add it on top without any role.
        if self.use_system_prompt:

            text = messages[0]["content"]
            prompt += f"{text}"

            for message in messages[1:]:
                role_prompt = self.role_to_prompt[message["role"]]
                prompt += f"{role_prompt} {message['content']}"

        else:
            text = messages[0]["content"]
            prompt += f"{self.role_to_prompt['user']} {text}"

            text = messages[1]["content"]
            prompt += f"\n\n{text}"

            for message in messages[2:]:
                role_prompt = self.role_to_prompt[message["role"]]
                prompt += f"{role_prompt} {message['content']}"

        return prompt+f"\n\n{self.role_to_prompt['assistant']}"


    def chat(self):
        t = self.messages_to_prompt(self.conversation)

        completion = self.anthropic.completions.create(
            model=self.model,
            max_tokens_to_sample=400,
            temperature=0,
            prompt=t,
        )
        time.sleep(1)
        return completion.completion

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})

    def set_state(self, state_dict):
        self.conversation = state_dict["conversation"]
        self.run_epoch_time_ms = state_dict["run_epoch_time_ms"]

    def dump_conversation(self, file_name):
        with open(file_name, "w") as f:
            for index, text in enumerate(self.conversation):
                c = text["content"].replace("\n", " ")

                if index % 2 == 0:
                    f.write(f"= = = = = Iteration {index // 2} = = = = =\n\n")
                    f.write(f'{text["role"]}: {c}' "\n\n")
                else:
                    f.write(f'\t\t{text["role"]}: {c}' "\n\n")





