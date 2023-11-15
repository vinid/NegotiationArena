import json
import logging
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Resources:
    resource_dict: dict = None

    @classmethod
    def from_string(cls, string: str):
        resource_dict = eval(string)
        return cls(resource_dict)

    def __str__(self):
        res = [f"'{k}': {v}" for k, v in self.resource_dict.items()]
        return "{" + ", ".join(res) + "}"

    def value(self):
        return sum(self.resource_dict.values())

    def to_prompt(self):
        res = [f"{k}: {v}" for k, v in self.resource_dict.items()]
        return ", ".join(res)

    def available_items(self):
        return list(self.resource_dict.keys())

    def __eq__(self, other):
        return self.resource_dict == other.resource_dict

    def check_transaction_legal(self, resource):
        return all(self.resource_dict.get(k, 0) - v >= 0 for k, v in resource.resource_dict.items())

    def equal(self, other):
        return self == other

    def __sub__(self, other):
        new_dict = defaultdict(int)
        for k, v in self.resource_dict.items():
            new_dict[k] += v
        for k, v in other.resource_dict.items():
            new_dict[k] -= v
        return Resources(new_dict)

    def __add__(self, other):
        new_dict = defaultdict(int)
        for k, v in self.resource_dict.items():
            new_dict[k] += v
        for k, v in other.resource_dict.items():
            new_dict[k] += v
        return Resources(new_dict)

    def get(self, key, default=None):
        return self.resource_dict.get(key, default)
