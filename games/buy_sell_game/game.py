from negobench.alternating_game import AlternatingGameEndsOnTag
from negobench.game_objects.resource import Resources
from negobench.constants import (
    REASONING_TAG,
    PLAYER_ANSWER_TAG,
    MESSAGE_TAG,
    PROPOSAL_COUNT_TAG,
    PROPOSED_TRADE_TAG,
    RESOURCES_TAG,
    GOALS_TAG,
    ACCEPTING_TAG,
)
from negobench.utils import extract_multiple_tags
from games.buy_sell_game.prompt import buy_sell_prompt
from negobench.parser import ExchangeGameDefaultParser
from negobench.agent_message import AgentMessage


class BuySellGameDefaultParser(ExchangeGameDefaultParser):
    def __init__(self):
        super().__init__()

    def instantiate_prompt(
        self,
        resources_in_game,
        initial_resources,
        goal,
        number_of_proposals,
        social_behaviour,
    ):
        return buy_sell_prompt(
            resources_in_game,
            initial_resources,
            goal,
            number_of_proposals,
            social_behaviour,
        )

    def parse(self, response):
        (
            resources,
            goal,
            reasoning,
            answer,
            message,
            proposal_count,
            trade,
        ) = extract_multiple_tags(
            response,
            [
                RESOURCES_TAG,
                GOALS_TAG,
                REASONING_TAG,
                PLAYER_ANSWER_TAG,
                MESSAGE_TAG,
                PROPOSAL_COUNT_TAG,
                PROPOSED_TRADE_TAG,
            ],
        )
        resources = Resources.from_string(resources)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)

        ms = AgentMessage()

        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        ms.add_secret(RESOURCES_TAG, resources)
        ms.add_secret(GOALS_TAG, goal)
        ms.add_secret(REASONING_TAG, reasoning)
        ms.add_secret(PROPOSAL_COUNT_TAG, proposal_count)

        return ms


class BuySellGame(AlternatingGameEndsOnTag):
    def __init__(
        self,
        resources_support_set,
        player_goals,
        player_initial_resources,
        player_social_behaviour,
        player_roles,
        game_interface=None,
        **kwargs
    ):
        super().__init__(end_tag=ACCEPTING_TAG, **kwargs)
        self.game_state = [
            {
                "current_iteration": "START",
                "turn": "None",
                "settings": dict(
                    resources_support_set=resources_support_set,
                    player_goals=player_goals,
                    player_initial_resources=player_initial_resources,
                    player_social_behaviour=player_social_behaviour,
                    player_roles=player_roles,
                    player_valuation=[g.get_valuation() for g in player_goals],
                ),
            }
        ]
        self.resources_support_set = resources_support_set
        self.player_goals = player_goals
        self.player_initial_resources = player_initial_resources
        self.player_social_behaviour = player_social_behaviour
        self.player_roles = player_roles

        self.game_interface = (
            BuySellGameDefaultParser()
            if game_interface is None
            else game_interface
        )

        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.game_interface.instantiate_prompt(
                resources_in_game=settings[
                    "resources_support_set"
                ].only_keys(),
                initial_resources=settings["player_initial_resources"][idx],
                goal=settings["player_goals"][idx],
                number_of_proposals=self.iterations // 2 - 1,
                social_behaviour=settings["player_social_behaviour"][idx],
            )

            player.init_agent(game_prompt, settings["player_roles"][idx])

    def check_winner(self):
        end_state = self.game_state[-1]
        if int(end_state["current_iteration"]) <= 1:
            datum = dict(
                current_iteration="END",
                turn="None",
            )

            self.game_state.append(datum)
        else:
            player_response = end_state["player_public_info_dict"][
                PLAYER_ANSWER_TAG
            ]
            initial_resources = self.game_state[0]["settings"][
                "player_initial_resources"
            ]
            player_valuation = self.game_state[0]["settings"][
                "player_valuation"
            ]
            player_goals = self.game_state[0]["settings"]["player_goals"]
            proposed_trade = self.game_state[-2]["player_public_info_dict"][
                PROPOSED_TRADE_TAG
            ]

            if player_response == ACCEPTING_TAG:
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
                current_iteration="END",
                turn="None",
                summary=dict(
                    player_goals=player_goals,
                    initial_resources=initial_resources,
                    proposed_trade=proposed_trade,
                    player_valuation=player_valuation,
                    final_response=player_response,  # ACCEPT / REJECT / NONE
                    final_resources=final_resources,
                    player_outcome=outcome,
                ),
            )

            self.game_state.append(datum)
