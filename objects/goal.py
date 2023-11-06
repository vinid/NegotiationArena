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


class MaximisationGoal(Goal):

    goal = "Acquire as many resources as possible"

    def __str__(self):
        return self.goal

    def to_prompt(self):
        return self.goal

    def goal_reached(self, inital_resource: Resources, final_resources: Resources):
        return final_resources-inital_resource