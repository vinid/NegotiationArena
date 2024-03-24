import copy
from openai import OpenAI
import os

import os
import random
from ratbench.agents.agents import Agent
import time
from ratbench.constants import AGENT_TWO, AGENT_ONE
from ratbench.agents.agent_behaviours import SelfCheckingAgent
from copy import deepcopy

import google.generativeai as genai

class GeminiAgent(Agent):
    def __init__(
        self,
        model="gemini-pro",
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
        self.role_to_prompt = {
            "user": "user",
            "system": "model",
            "assistant": "model"
        }
        self.safe = [{
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    },
                ]
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        self.model = genai.GenerativeModel('gemini-pro')
        self.temperature = temperature
        self.max_tokens = max_tokens

    def init_agent(self, system_prompt, role):
        if AGENT_ONE in self.agent_name:
            # we use the user role to tell the assistant that it has to start.
            self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)
            self.update_conversation_tracking("user", role)

        elif AGENT_TWO in self.agent_name:
            system_prompt = system_prompt + role
            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
        else:
            raise "No Player 1 or Player 2 in role"

    def __deepcopy__(self, memo):
        """
        Deepcopy is needed because we cannot pickle the object.
        :param memo:
        :return:
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():

            if k == "model" and not isinstance(v, str):
                v = v.__class__.__name__
            setattr(result, k, deepcopy(v, memo))
        return result

    def chat(self):
        mex = self.transform_to_gemini(self.conversation)
        response = self.model.generate_content(mex, safety_settings=self.safe)

        return response.text

    def transform_to_gemini(self, messages_chatgpt):
        messages_gemini = []
        system_promt = ''
        for message in messages_chatgpt:
            if message['role'] == 'system':
                system_promt = message['content']
            elif message['role'] == 'user':
                messages_gemini.append({'role': 'user', 'parts': [message['content']]})
            elif message['role'] == 'assistant':
                messages_gemini.append({'role': 'model', 'parts': [message['content']]})
        if system_promt:
            messages_gemini[0]['parts'].insert(0, f"*{system_promt}*")

        return messages_gemini

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})


