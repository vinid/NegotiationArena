import json
import logging
from dataclasses import dataclass
from collections import defaultdict
from objects.resource import Resources
class Trade:

    def __init__(self, trade, raw_string=None):
        keys = sorted(list(trade.keys()))

        self.resources_from_first_agent = Resources(trade[keys[0]])
        self.resources_from_second_agent = Resources(trade[keys[1]])
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
        net_resource = self.resources_from_second_agent - self.resources_from_first_agent if direction_of_the_trade == 0 else self.resources_from_first_agent - self.resources_from_second_agent
        resources_after_trade = resources + net_resource
        return resources_after_trade

    def utility(self, resources, goal, direction_of_the_trade):
        net_resource = self.resources_from_second_agent - self.resources_from_first_agent if direction_of_the_trade == 0 else self.resources_from_first_agent - self.resources_from_second_agent
        resources_after_trade = resources + net_resource
        utility = resources_after_trade - goal

        return sum(list(utility.resource_dict.values()))

    def minimal_utility(self, resources, goal, direction_of_the_trade):
        net_resource = self.resources_from_second_agent - self.resources_from_first_agent if direction_of_the_trade == 0 else self.resources_from_first_agent - self.resources_from_second_agent
        resources_after_trade = resources + net_resource
        utility = resources_after_trade - goal

        return sum(-max(0, -u) for u in utility.resource_dict.values())

    def overall_utility(self, resources, goal, direction_of_the_trade):
        net_resource = self.resources_from_second_agent - self.resources_from_first_agent if direction_of_the_trade == 0 else self.resources_from_first_agent - self.resources_from_second_agent
        resources_after_trade = resources + net_resource
        utility = resources_after_trade - goal

        return sum(list(utility.resource_dict.values()))

    def to_prompt(self):
        return "Player 1 Gets {} ; Player 2 Gets {}".format(self.resources_from_first_agent.to_prompt(),
                                                                   self.resources_from_second_agent.to_prompt())

    def __str__(self):
        return "{{1: {}, 2: {}}}".format(self.resources_from_first_agent, self.resources_from_second_agent)

