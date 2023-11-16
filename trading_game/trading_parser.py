from game.parser import ParseRule, text_to_dict
from game.game_objects.resource import Resources
from game.game_objects.goal import ResourceGoal
from game.game_objects.trade import Trade

class ResourcesParseRule(ParseRule):
    def parse(self, response):
        contents = self.get_tag_contents(response).lstrip().rstrip()
        return Resources(text_to_dict(contents))

class GoalsParseRule(ParseRule):
    def parse(self, response):
        contents = self.get_tag_contents(response).lstrip().rstrip()
        return ResourceGoal(text_to_dict(contents))

class ProposedTradeParseRule(ParseRule):
    
    def parse_proposed_trade(self, s):
        trade = {}
        items = s.split(" Gives")
        for i in range(1, len(items)):
            item = items[i]
            prev_item = items[i - 1]
            player_id = str(prev_item[-2:].strip())
            subitem = item.split(" Player")[0].strip()
            try:
                resources = {k: float(v.replace(",", "").rstrip(".,;")) for k, v in
                             (item.split(": ") for item in subitem.split(", "))}
            except Exception as e:
                print(subitem)
                raise e
            trade[player_id] = resources
        return trade

    def parse(self, response):
        contents = self.get_tag_contents(response).lstrip().rstrip()
        if contents == 'WAIT':
            return contents
        return Trade(self.parse_proposed_trade(contents))
