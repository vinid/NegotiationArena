import json
import logging
from dataclasses import dataclass
from collections import defaultdict



def text_to_dict(s):
    return {k: int(v) for k, v in (item.split(": ") for item in s.split(", "))}


@dataclass
class Resources:
    resource_dict: dict = None

    def __str__(self):
        res = [f"'{k}': {v}" for k, v in self.resource_dict.items()]
        return "{" +  ", ".join(res) + "}"

    def value(self):
        return sum(self.resource_dict.values())

    def to_prompt(self):
        res = [f"{k}: {v}" for k, v in self.resource_dict.items()]
        return ", ".join(res)

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
    
class Trade:

    def __init__(self, trade):

        self.resources_from_one = Resources(trade[list(trade.keys())[0]])
        self.resources_from_two = Resources(trade[list(trade.keys())[1]])

    def can_offer(self, resources):
        return resources.check_transaction_legal(self.resources_from_one)

    def can_accept(self, resources):
        return resources.check_transaction_legal(self.resources_from_two)
    
    def utility(self, marginal_utility_1, marginal_utility_2):
        
        net_resource = self.resources_from_two - self.resources_from_one

        return {
            1: sum([ v  * marginal_utility_1.get(k,0) for k,v in net_resource.resource_dict.items()]), 
            2: sum([ -v  * marginal_utility_2.get(k,0) for k,v in net_resource.resource_dict.items()]), 
        }
        

    def to_prompt(self):
        return "Player 1 Gives {} ; Player 2 Gives {}".format(self.resources_from_one.to_prompt(), self.resources_from_two.to_prompt())
    
    def __str__(self):
        return "{{1: {}, 2: {}}}".format(self.resources_from_one, self.resources_from_two)

@dataclass
class Goal(Resources):

    def goal_reached(self, resources: Resources):
        return all(resources.resource_dict.get(k, 0) >= v for k, v in self.resource_dict.items())


def parse_proposed_trade(s):
    trade = {}
    items = s.split(" Gives:")
    for i in range(1, len(items)):
        item = items[i]
        prev_item = items[i - 1]
        player_id = int(prev_item[-2:].strip())
        subitem = item.split(" Player")[0].strip()
        try:
            resources = {k: float(v.replace(",", "")) for k, v in (item.split(": ") for item in subitem.split(", "))}
        except Exception as e:
            print(subitem)
            raise e

        trade[player_id] = resources
    return trade


class StateTracker:

    def __init__(self):
        self.proposed_trade = None
        self.received_trade = None
        self.resources = None
        self.player_response = None
        self.marginal_utility = None
        self.received_trade_utility = None
        self.proposed_trade_utility = None
        self.iteration = None


    def set_proposed_trade(self, trade):
        self.proposed_trade = trade

    def set_resources(self, resources):
        self.resources = resources

    def set_player_response(self, response):
        self.player_response = response

    def __str__(self):
        return f"StateTracker: {self.resources}, {self.proposed_trade}, {self.player_response}"



def parse_response(response):
    lines = response.split("\n")

    my_resources = None
    player_response = None
    proposed_trade = None
    for l in lines:
        if l.startswith("MY RESOURCES:"):
            my_resources = (Resources(text_to_dict(l.split("RESOURCES: ")[1])))

        elif l.startswith("NEWLY PROPOSED TRADE:"):
            trade = l.split("NEWLY PROPOSED TRADE:")[1].strip()
            proposed_trade = (Trade(parse_proposed_trade(trade)))
            #lines_to_pass["proposed_trade"] = l

        elif l.startswith("PLAYER RESPONSE: "):
            player_response = (l.split("PLAYER RESPONSE: ")[1])
            #lines_to_pass["player_response"] = l
        else:
            logging.info(f"..::UNPARSED: {l}::..")
            continue
        
    return my_resources, player_response, proposed_trade
