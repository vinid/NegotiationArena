from dataclasses import dataclass


@dataclass
class Role:
    first_agent = "user"
    second_agent = "assistant"


@dataclass
class Resources:
    resource_dict: dict = None

    def to_prompt(self):
        return "You currently have the following resources: " + ", ".join([f"{v} {k}" for k, v in self.resource_dict.items()])


@dataclass
class Goal:
    resource_dict: dict = None

    def goal_reached(self, resources: Resources):
        return all(resources.resource_dict.get(k, 0) >= v for k, v in self.resource_dict.items())

    def to_prompt(self):
        return "By the end of the negotiation you need to have: " + ", ".join([f"{v} {k}" for k, v in self.resource_dict.items()])


