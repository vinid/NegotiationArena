import json
import logging
from dataclasses import dataclass
from collections import defaultdict
from objects.resource import Resources

@dataclass
class Goal(Resources):

    def goal_reached(self, resources: Resources):
        return all(resources.resource_dict.get(k, 0) >= v for k, v in self.resource_dict.items())

