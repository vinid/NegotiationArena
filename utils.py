from dataclasses import dataclass
from collections import defaultdict

def resource_str_fn(resources):
    res = [f"{k}: {v}" for k, v in resources.items()]
    return ", ".join(res)

def text_to_dict(s):
    return {k: int(v) for k, v in (item.split(": ") for item in s.split(", "))}



@dataclass
class Resources:
    resource_dict: dict = None

    def to_prompt(self):
        return resource_str_fn(self.resource_dict)

    def check_transaction_legal(self, resource):
        return all(self.resource_dict.get(k, 0) - v >= 0 for k, v in resource.resource_dict.items())

    def equal(self, other):
        return self.resource_dict == other.resource_dict

    def __add__(self, other):
        new_dict = defaultdict(int)
        for k, v in self.resource_dict.items():
            new_dict[k] += v
        for k, v in other.resource_dict.items():
            new_dict[k] += v
        return Resources(new_dict)


class Trade:

    def __init__(self, trade):

        self.resources_from_one = Resources(trade[list(trade.keys())[0]])
        self.resources_from_two = Resources(trade[list(trade.keys())[1]])

    def can_offer(self, resources):
        return resources.check_transaction_legal(self.resources_from_one)

    def can_accept(self, resources):
        return resources.check_transaction_legal(self.resources_from_two)

@dataclass
class Goal(Resources):

    def goal_reached(self, resources: Resources):
        return all(resources.resource_dict.get(k, 0) >= v for k, v in self.resource_dict.items())

    def to_prompt(self):
        return resource_str_fn(self.resource_dict)


def parse_proposed_trade(s):
    trade = {}
    items = s.split(" Gives:")
    for i in range(1, len(items)):
        item = items[i]
        prev_item = items[i - 1]
        player_id = int(prev_item[-2:].strip())
        subitem = item.split(" Player")[0].strip()
        resources = {k: int(v.replace(",", "")) for k, v in (item.split(": ") for item in subitem.split(", "))}
        trade[player_id] = resources
    return trade

def parse_response(response):
    lines = response.split("\n")
    lines_to_pass = defaultdict(list)
    structured_state = {}
    for l in lines:
        if l.startswith("MY RESOURCES:"):
            structured_state["resources"] = Resources(text_to_dict(l.split("RESOURCES: ")[1]))

        elif l.startswith("PROPOSED TRADE:"):
            trade = l.split("PROPOSED TRADE:")[1].strip()
            structured_state["proposed_trade"] = Trade(parse_proposed_trade(trade))
            lines_to_pass["proposed_trade"] = l

        elif l.startswith("NEWLY PROPOSED TRADE:"):
            trade = l.split("NEWLY PROPOSED TRADE:")[1].strip()
            structured_state["proposed_trade"] = Trade(parse_proposed_trade(trade))
            lines_to_pass["proposed_trade"] = l

        elif l.startswith("PLAYER RESPONSE: "):
            structured_state["player_response"] = l.split("PLAYER RESPONSE: ")[1]
            lines_to_pass["player_response"] = l
        else:
            print(f"..::UNPARSED: {l}::..")
            continue

    return lines_to_pass["proposed_trade"], lines_to_pass["player_response"], structured_state
