import sys
sys.path.append('.')
import os
from game.logging import GameEncoder
from game.game import AlternatingGame, CommunicationGame
from game.constants import (
    MESSAGE_TAG,
    RESOURCES_TAG,
    GOALS_TAG,
    PLAYER_RESPONSE_TAG,
    PROPOSED_TRADE_TAG,
    REASONING_TAG,
)
from game.parser import UnformattedParseRule
from trading_game.trading_game import TradingGame
from buyer_seller_game.buyer_seller_prompts import BuyerSellerPrompt
from trading_game.trading_parser import ResourcesParseRule, GoalsParseRule
from buyer_seller_game.buyer_seller_parser import ProposedTradeParseRule

class BuyerSellerGame(TradingGame):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def game_prompt(self):
        return BuyerSellerPrompt


    def format_guide(self):
        self.parser.add_parse_rules([
            # ResourcesParseRule(RESOURCES_TAG),
            UnformattedParseRule(GOALS_TAG),
            ProposedTradeParseRule(PROPOSED_TRADE_TAG),
            UnformattedParseRule(PLAYER_RESPONSE_TAG),  
        ])

        # update format prompt
    # def check_winner(self):
    #     end_state = self.game_state[-1]
    #     player_response = end_state['response'][PLAYER_RESPONSE_TAG]
    #     initial_resources = self.game_state[0]['settings']['player_initial_resources']
    #     player_goals = self.game_state[0]['settings']['player_goals']
    #     proposed_trade = self.game_state[-2]['response'][PROPOSED_TRADE_TAG]

    #     if player_response == 'ACCEPTED':
    #         # get proposed trade
    #         final_resources = [ proposed_trade.execute_trade(res, idx) for idx, res in enumerate(initial_resources)]
    #     else:
    #         final_resources = initial_resources
        
    #     outcome = [ goal.goal_reached(final) for goal,final in zip(player_goals, final_resources)]
    #     datum = dict(
    #         iteration='END',
    #         turn='None',
    #         summary=dict(
    #             player_goals=player_goals,
    #             initial_resources=initial_resources,
    #             proposed_trade=proposed_trade,
    #             final_response=player_response, # ACCEPT / REJECT / WAIT
    #             final_resources=final_resources,
    #             player_outcome=outcome
    #         )
    #     )
        
    #     self.game_state.append(datum)
