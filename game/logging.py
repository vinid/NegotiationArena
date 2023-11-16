import json
from game.game_objects.resource import Resources
from game.game_objects.goal import Goal
from game.game_objects.trade import Trade

class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Resources):
            return obj.resource_dict
        if isinstance(obj, Goal):
            return obj.goal
        if isinstance(obj, Trade):
            return {k: self.default(v) for k,v in obj.json().items()}
        return super().default(obj)

