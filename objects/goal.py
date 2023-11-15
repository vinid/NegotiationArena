import json
import logging
from dataclasses import dataclass
from collections import defaultdict
from objects.resource import Resources
from abc import abstractmethod


class Goal:

    def __init__(self):
        pass

    @abstractmethod
    def goal_reached(self):
        pass


@dataclass
class ResourceGoal(Goal, Resources):

    def goal_reached(self, resources: Resources):
        return all(resources.resource_dict.get(k, 0) >= v for k, v in self.resource_dict.items())

    def get_minimal_offer(self, resources: Resources):
        return self - resources

    def make_better_offer(self, past_offer, resources):
        minimal_offer = self.get_minimal_offer(resources)

        # this was originally in the Resource class but honestly does not fell the right thing to have there
        available_to_sell = {k: v for k, v in minimal_offer.resource_dict.items() if v < 0}
        in_need_for = {k: v for k, v in minimal_offer.resource_dict.items() if v > 0}

        if available_to_sell:
            available_to_sell["X"] = available_to_sell["X"] + 1



        return available_to_sell







class MaximisationGoal(Goal):

    goal = "Acquire as many resources as possible"

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, inital_resource: Resources, final_resources: Resources):
        return final_resources-inital_resource


class UltimatumGoal(Goal):

    goal = "Find and agreement on how to split the resources otherwise both players are not going to win anything."

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, inital_resource: Resources, final_resources: Resources):
        return final_resources-inital_resource

class BuyerGoal(Goal):

    goal = "Sell resources but try to get as much money as possible"

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, inital_resource: Resources, final_resources: Resources):
        return final_resources-inital_resource

class SellerGoal(Goal):

    goal = "Buy resources but at a reasonable price"

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, inital_resource: Resources, final_resources: Resources):
        return final_resources-inital_resource
