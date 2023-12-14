import copy
import openai
import os
import random
from ratbench.agents.agents import Agent
import time
from ratbench.constants import AGENT_TWO, AGENT_ONE
from ratbench.agents.agent_behaviours import SelfCheckingAgent


class ChatGPTAgent(Agent):
    def __init__(
        self,
        model="gpt-4-1106-preview",
        temperature=0.7,
        max_tokens=400,
        seed=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.run_epoch_time_ms = str(round(time.time() * 1000))
        self.model = model
        self.conversation = []
        self.prompt_entity_initializer = "system"
        self.seed = (
            int(self.run_epoch_time_ms) + random.randint(0, 2**16)
            if seed is None
            else seed
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def init_agent(self, system_prompt, role):
        if AGENT_ONE in self.agent_name:
            # we use the user role to tell the assistant that it has to start.

            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
            self.update_conversation_tracking("user", role)
        elif AGENT_TWO in self.agent_name:
            system_prompt = system_prompt + role
            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
        else:
            raise "No Player 1 or Player 2 in role"

    def chat(self):
        chat = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            seed=self.seed,
        )

        return chat["choices"][0]["message"]["content"]

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})


class SelfCheckingChatGPTAgent(ChatGPTAgent, SelfCheckingAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
