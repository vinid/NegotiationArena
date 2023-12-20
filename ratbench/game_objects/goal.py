import json
import logging
from dataclasses import dataclass
from collections import defaultdict
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.valuation import Valuation
from abc import abstractmethod
from ratbench.constants import *


class Goal:
    def __init__(self):
        pass

    @abstractmethod
    def goal_reached(self):
        pass

    @abstractmethod
    def json(self):
        pass


@dataclass
class ResourceGoal(Goal, Resources):
    def goal_reached(self, resources: Resources):
        return all(
            resources.resource_dict.get(k, 0) >= v
            for k, v in self.resource_dict.items()
        )

    def get_minimal_offer(self, resources: Resources):
        return self - resources

    def make_better_offer(self, past_offer, resources):
        minimal_offer = self.get_minimal_offer(resources)

        # this was originally in the Resource class but honestly does not fell the right thing to have there
        available_to_sell = {
            k: v for k, v in minimal_offer.resource_dict.items() if v < 0
        }
        in_need_for = {k: v for k, v in minimal_offer.resource_dict.items() if v > 0}

        if available_to_sell:
            available_to_sell["X"] = available_to_sell["X"] + 1

        return available_to_sell

    def json(self):
        return {"_type": "resource_goal", "_value": self.resource_dict}


class MaximisationGoal(Goal):
    goal = "Acquire as many resources as possible"

    def __init__(self, inital_resources: Resources):
        self.inital_resources = inital_resources

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, final_resources: Resources):
        return final_resources - self.inital_resources

    def json(self):
        return {"_type": "maximisation_goal", "_value": self.inital_resources}


class UltimatumGoal(Goal):
    goal = ""

    def __str__(self):
        return self.goal

    def __repr__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, inital_resource: Resources, final_resources: Resources):
        return final_resources - inital_resource

    def json(self):
        return {"_type": "ultimatum_goal", "_value": self.goal}


class BuyerGoal(Goal):
    def __init__(self, willingness_to_pay: Valuation):
        super().__init__()
        self.willingness_to_pay = willingness_to_pay
        self.goal = f"Buy resources with <{MONEY_TOKEN}>. You are willing to pay at most {willingness_to_pay} for the resources."

    def __repr__(self):
        return self.goal

    def get_valuation(self):
        return self.willingness_to_pay

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def json(self):
        return {"_type": "buyer_goal", "_value": self.willingness_to_pay.json()}


class SellerGoal(Goal):
    def __init__(self, cost_of_production: Valuation):
        super().__init__()
        self.cost_of_production = cost_of_production
        self.goal = f"Sell resources for <{MONEY_TOKEN}>. It costed {self.cost_of_production} to produce the resources"

    def __repr__(self):
        return self.goal

    def get_valuation(self):
        return self.cost_of_production

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def json(self):
        return {"_type": "seller_goal", "_value": self.cost_of_production.json()}
