from abc import ABC, abstractmethod
import copy
from ratbench.constants import *
from copy import deepcopy


class Agent(ABC):
    """
    Representing a Single LLM Agent
    """

    agent_class = __qualname__

    def __init__(self, **kwargs):
        self.model = None
        self.agent_name = None
        self.prompt_entity_initializer = None

        if self.agent_name not in [AGENT_ONE, AGENT_TWO]:
            raise ValueError(f"Agent name must be either {AGENT_ONE} or {AGENT_TWO}")

    @abstractmethod
    def chat(self):
        pass

    @abstractmethod
    def update_conversation_tracking(self, entity, message):
        pass

    @abstractmethod
    def get_state(
            self,
    ):
        """
        agent state refers to all information necessary to reproduce agent at a given time
        """
        pass

    # TODO: We don't use this for now
    # @abstractmethod
    def set_state(self):
        pass

    def init_agent(self, system_prompt, role):
        # clear conversation
        self.conversation = []

        system_prompt = system_prompt + role

        self.update_conversation_tracking(self.prompt_entity_initializer, system_prompt)

    def think(self):
        # call agent / make agent think
        response = self.chat()

        # update agent history
        self.update_conversation_tracking("assistant", response)

        return response

    def step(self, message):
        """
        Make agent take a step in a ratbench:

        1. get state from ratbench
        2. genereate a response to state
        3. return response

        """

        if message:
            self.update_conversation_tracking("user", message)

        response = self.think()

        return response

    def get_state(self):
        try:
            c = {
                "class": self.__class__.__name__,
                **deepcopy(self).__dict__,
            }
        except Exception as e:
            print(e)
            for k,v in self.__dict__.items():
                print(k, v, type(v))
            exit()

        return c

    @abstractmethod
    def set_state(self):
        pass

    @classmethod
    def from_dict(cls, state_dict):
        state_dict = copy.deepcopy(state_dict)
        class_name = state_dict.pop("class")
        subclasses = cls.get_all_subclasses()
        constructor = (
            cls
            if class_name == cls.__name__
            else next((sub for sub in subclasses if sub.__name__ == class_name), None)
        )
        if constructor:
            obj = constructor(**state_dict)
            obj.set_state(state_dict)
            return obj
        else:
            raise ValueError(f"Unknown subclass: {class_name}")

    @classmethod
    def get_all_subclasses(cls):
        subclasses_set = set()
        # Recursively get subclasses of subclasses
        for subclass in cls.__subclasses__():
            subclasses_set.add(subclass)
            subclasses_set.update(subclass.get_all_subclasses())

        return list(subclasses_set)
