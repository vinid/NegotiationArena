from game.parser import ParseRule, text_to_dict
from game.game_objects.resource import Resources
from game.game_objects.goal import ResourceGoal
from game.game_objects.trade import Trade


# class ProposedTradeParseRule(ParseRule):
#     def parse_proposed_trade(self, s):
#         print(s)
#         trade = {}
#         trade_one_two = s.split("Gives")[-1]
#         for idx, t in enumerate(trade_one_two):
#             items = t.split(":")[0].lstrip(" ").rstrip(" ")
#             item =
#             money = t.split(":")[1].lstrip(" ").rstrip(" ")
#             trade[idx + 1] = {item: money}

# #         return trade

#     def parse(self, response):
#         contents = self.get_tag_contents(response).lstrip().rstrip()
#         if contents == "WAIT":
#             return contents

#         return Trade(self.parse_proposed_trade(contents))
