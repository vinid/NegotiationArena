import json
from game.game_objects.resource import Resources
from game.game_objects.goal import *
from game.game_objects.trade import Trade
from game.game_objects.valuation import Valuation
from game.agents.agents import Agent
from game.interface import GameInterface


class GameDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "_type" not in obj:
            return obj
        type = obj["_type"]
        if type == "resource":
            return Resources(obj["_value"])
        if type == "goal":
            goal_type = obj["_value"]["_type"]
            goal_val = obj["_value"]["_value"]
            if goal_type == "resource_goal":
                return ResourceGoal(goal_val)
            elif goal_type == "maximisation_goal":
                return MaximisationGoal()
            elif goal_type == "ultimatum_goal":
                return UltimatumGoal()
            elif goal_type == "buyer_goal":
                return BuyerGoal()
            elif goal_type == "seller_goal":
                return SellerGoal()

        if type == "trade":
            return Trade({k: v.resource_dict for k, v in obj["_value"].items()})
        # if type == "valuation":
        #     pass
        # return parser.parse(obj["value"])
        return obj


class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Goal):
            return {"_type": "goal", "_value": obj.json()}

        if isinstance(obj, Trade):
            return {
                "_type": "trade",
                "_value": {k: self.default(v) for k, v in obj.json().items()},
            }

        if isinstance(obj, Valuation):
            return {"_type": "valuation", "_value": obj.valuation_dict}

        if isinstance(obj, Resources):
            return {"_type": "resource", "_value": obj.resource_dict}

        if isinstance(obj, Agent):
            return obj.get_state()

        if isinstance(obj, GameInterface):
            return {"class": obj.__class__.__name__}
        return super().default(obj)
