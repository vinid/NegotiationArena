import sys

sys.path.append(".")
import os
from game.logging import GameEncoder
from game.game import AlternatingGame, CommunicationGame
from game.constants import (
    MESSAGE_TAG,
    RESOURCES_TAG,
    GOALS_TAG,
    PLAYER_ANSWER_TAG,
    PROPOSED_TRADE_TAG,
    REASONING_TAG,
)
from game.prompt_builder import Prompt

from game.parser import UnformattedParseRule, PassThroughParseRule
from games.trading_game.trading_game import TradingGame
from games.trading_game.trading_parser import (
    ResourcesParseRule,
    GoalsParseRule,
    ProposedTradeParseRule,
)

from games.buyer_seller_game.buyer_seller_prompts import BuyerSellerPrompt

# from games.buyer_seller_game.buyer_seller_parser import ProposedTradeParseRule


class BuyerSellerGame(TradingGame):
    def __init__(self, player_valuation, **kwargs):
        super().__init__(player_valuation=player_valuation, **kwargs)

        self.game_state = [
            {
                "iteration": "START",
                "turn": "None",
                "settings": dict(kwargs, player_valuation=player_valuation),
            }
        ]

    @property
    def game_prompt(self):
        return BuyerSellerPrompt

    def init_parser(self):
        self.global_parser.add_parse_rules(
            [
                UnformattedParseRule(GOALS_TAG),
                UnformattedParseRule(PLAYER_ANSWER_TAG),
                ProposedTradeParseRule(PROPOSED_TRADE_TAG),
            ]
        )

        self.public_parser.add_parse_rules(
            [
                PassThroughParseRule(PLAYER_ANSWER_TAG),
                PassThroughParseRule(PROPOSED_TRADE_TAG),
            ]
        )

        # update format prompt

    def check_winner(self):
        end_state = self.game_state[-1]
        player_response = end_state["response"][PLAYER_RESPONSE_TAG]
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_valuation = self.game_state[0]["settings"]["player_valuation"]
        player_goals = self.game_state[0]["settings"]["player_goals"]
        proposed_trade = self.game_state[-2]["response"][PROPOSED_TRADE_TAG]

        if player_response == "ACCEPTED":
            # get proposed trade
            final_resources = [
                proposed_trade.execute_trade(res, idx)
                for idx, res in enumerate(initial_resources)
            ]
        else:
            final_resources = initial_resources

        outcome = [
            v.value(final - initial)
            for v, initial, final in zip(
                player_valuation, initial_resources, final_resources
            )
        ]
        datum = dict(
            iteration="END",
            turn="None",
            summary=dict(
                player_goals=player_goals,
                initial_resources=initial_resources,
                proposed_trade=proposed_trade,
                final_response=player_response,  # ACCEPT / REJECT / WAIT
                final_resources=final_resources,
                player_outcome=outcome,
            ),
        )

        self.game_state.append(datum)
