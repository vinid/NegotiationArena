"""
Representation of how much agent values resources as a unit of `MONEY_TOKEN`
"""

from dataclasses import dataclass
from game.constants import *
from game.game_objects.resource import Resources


@dataclass
class Valuation:
    valuation_dict: dict = None
    # e.g. {X:2, Y:4, M: 10} where 2 => 2M, 4 => 4M

    def value(self, resources: Resources):
        val_of_resources = 0
        for k, v in resources.resource_dict.items():
            if k != MONEY_TOKEN:
                val_of_resources += self.valuation_dict[k] * v
            else:
                val_of_resources += v
        return val_of_resources

    def to_prompt(self):
        res = [f"{k}: {v}" for k, v in self.valuation_dict.items()]
        return ", ".join(res)


def __str__(self):
    res = [f"'{k}': {v}" for k, v in self.resource_dict.items()]
    return "{" + ", ".join(res) + "}"


def __repr__(self):
    return self.__str__(self)


def json(self):
    return self.valuation_dict
