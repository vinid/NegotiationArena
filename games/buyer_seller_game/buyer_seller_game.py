import sys

sys.path.append(".")
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
                UnformattedParseRule(PLAYER_RESPONSE_TAG),
                ProposedTradeParseRule(PROPOSED_TRADE_TAG),
            ]
        )

        self.public_parser.add_parse_rules(
            [
                PassThroughParseRule(PLAYER_RESPONSE_TAG),
                PassThroughParseRule(PROPOSED_TRADE_TAG),
            ]
        )

    def init_players(self):
        for idx, player in enumerate(self.players):
            game_prompt = self.game_prompt(
                self.game_state[0]["settings"]["resources_support_set"],
                agent_initial_resources=self.game_state[0]["settings"][
                    "player_initial_resources"
                ][idx],
                agent_valuation=self.game_state[0]["settings"]["player_valuation"][idx],
                agent_goal=self.game_state[0]["settings"]["player_goals"][idx],
                n_rounds=self.iterations // 2 - 1,
                agent_social_behaviour=self.game_state[0]["settings"][
                    "player_social_behaviour"
                ][idx],
            )
            player.init_agent(
                game_prompt
                + self.global_parser.get_response_format_prompt()
                + Prompt([self.game_state[0]["settings"]["player_roles"][idx]])
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
