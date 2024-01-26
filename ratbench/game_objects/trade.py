import json
import logging
from dataclasses import dataclass
from collections import defaultdict
from ratbench.game_objects.resource import Resources


class Trade:
    def __init__(self, trade, raw_string=None):
        self.keys = sorted(list(trade.keys()), reverse=True)

        self.resources_from_first_agent = Resources(trade[self.keys[0]])
        self.resources_from_second_agent = Resources(trade[self.keys[1]])
        self.raw_string = raw_string

    @classmethod
    def from_string(cls, string: str):
        trade = eval(string)
        return cls(trade)

    def can_offer(self, resources):
        return resources.check_transaction_legal(self.resources_from_first_agent)

    def can_accept(self, resources):
        return resources.check_transaction_legal(self.resources_from_second_agent)

    def execute_trade(self, resources, direction_of_the_trade):
        net_resource = (
            self.resources_from_second_agent - self.resources_from_first_agent
            if direction_of_the_trade == 0
            else self.resources_from_first_agent - self.resources_from_second_agent
        )
        resources_after_trade = resources + net_resource
        return resources_after_trade

    def utility(self, resources, goal, direction_of_the_trade):
        net_resource = (
            self.resources_from_second_agent - self.resources_from_first_agent
            if direction_of_the_trade == 0
            else self.resources_from_first_agent - self.resources_from_second_agent
        )
        resources_after_trade = resources + net_resource
        utility = resources_after_trade - goal

        return sum(list(utility.resource_dict.values()))

    def minimal_utility(self, resources, goal, direction_of_the_trade):
        net_resource = (
            self.resources_from_second_agent - self.resources_from_first_agent
            if direction_of_the_trade == 0
            else self.resources_from_first_agent - self.resources_from_second_agent
        )
        resources_after_trade = resources + net_resource
        utility = resources_after_trade - goal

        return sum(-max(0, -u) for u in utility.resource_dict.values())

    def overall_utility(self, resources, goal, direction_of_the_trade):
        net_resource = (
            self.resources_from_second_agent - self.resources_from_first_agent
            if direction_of_the_trade == 0
            else self.resources_from_first_agent - self.resources_from_second_agent
        )
        resources_after_trade = resources + net_resource
        utility = resources_after_trade - goal

        return sum(list(utility.resource_dict.values()))

    def __str__(self):
        a1 = self.keys[0]
        a2 = self.keys[1]
        return f"Player {a1} Gives {self.resources_from_first_agent} | Player {a2} Gives {self.resources_from_second_agent}"

    def __repr__(self):
        a1 = self.keys[0]
        a2 = self.keys[1]
        return f"Player {a1} Gives {self.resources_from_first_agent} | Player {a2} Gives {self.resources_from_second_agent}"

    def json(self):
        return {
            self.keys[0]: self.resources_from_first_agent,
            self.keys[1]: self.resources_from_second_agent,
        }
