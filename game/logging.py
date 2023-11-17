import json
from game.game_objects.resource import Resources
from game.game_objects.goal import Goal
from game.game_objects.trade import Trade
from game.game_objects.valuation import Valuation
from game.agents.agents import Agent


class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Resources):
            return obj.resource_dict

        if isinstance(obj, Goal):
            return obj.goal

        if isinstance(obj, Trade):
            return {k: self.default(v) for k, v in obj.json().items()}

        if isinstance(obj, Valuation):
            return obj.valuation_dict

        if isinstance(obj, Agent):
            return obj.get_state()

        return super().default(obj)
