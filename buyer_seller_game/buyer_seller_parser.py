from game.parser import ParseRule, text_to_dict
from game.game_objects.resource import Resources
from game.game_objects.goal import ResourceGoal
from game.game_objects.trade import Trade

class ProposedTradeParseRule(ParseRule):
    
    def parse_proposed_trade(self, s):
        trade = {}
        items = s.split(" Gives")
        money = items[1].split(':')[-1].lstrip(' ').rstrip(' ')
        return { 1:{ },2:{'Money': money} }

    def parse(self, response):
        contents = self.get_tag_contents(response).lstrip().rstrip()
        if contents == 'WAIT':
            return contents
        return Trade(self.parse_proposed_trade(contents))
