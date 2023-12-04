import sys
from ratbench.alternating_game import AlternatingGame
from games.ultimatum.one_shot_ultimatum.interface import UltimatumOneShotGameInterface
from ratbench.constants import *


class UltimatumOneShotGame(AlternatingGame):
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
        super().__init__(**kwargs)

        if game_interface is None:
            self.game_interface = UltimatumOneShotGameInterface()


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
                ),
            }
        ]
        self.resources_support_set = resources_support_set
        self.player_goals = player_goals
        self.player_initial_resources = player_initial_resources
        self.player_social_behaviour = player_social_behaviour
        self.player_roles = player_roles


        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.game_interface.get_prompt(
                player_1_initial_resources=settings["player_initial_resources"][0].only_keys(),
                resources_in_game=settings["resources_support_set"],
                initial_resources=settings["player_initial_resources"][idx],
                social_behaviour=settings["player_social_behaviour"][idx],
            )
            player.init_agent(game_prompt, settings["player_roles"][idx])

    def game_over(self):
        """
        ratbench over logic based on ratbench state
        """
        state = self.game_state[-1]
        if state:
            response = state["player_public_info_dict"].get(PLAYER_ANSWER_TAG, REFUSING_OR_WAIT_TAG)
            iteration = state.get("current_iteration", 0)
            if response == ACCEPTING_TAG or iteration == self.iterations:
                return True

        return False

    def check_winner(self):
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_goals = self.game_state[0]["settings"]["player_goals"]

        # the last state contains the end ratbench state of the accepted proposal
        end_state = self.game_state[-1]

        # if there are not enough iterations winner is meaningless
        if end_state["current_iteration"] <= 1:
                    datum = dict(
                        current_iteration="END",
                        turn="None",
                    )

                    self.game_state.append(datum)
                    return


        # and because of the above the accepted trade is the second to last one
        proposed_trade = self.game_state[-2]["player_public_info_dict"][
            PROPOSED_TRADE_TAG
        ]

        player_answer = end_state["player_public_info_dict"][PLAYER_ANSWER_TAG]

        # if the player did not reach an agreement, they keep their initial resources
        if player_answer == ACCEPTING_TAG:
            # get proposed trade
            final_resources = [
                proposed_trade.execute_trade(res, idx)
                for idx, res in enumerate(initial_resources)
            ]
        else:
            final_resources = initial_resources

        outcome = [
            (final - initial)
            for initial, final in zip(initial_resources, final_resources)
        ]
        datum = dict(
            current_iteration="END",
            turn="None",
            summary=dict(
                player_goals=player_goals,
                initial_resources=initial_resources,
                proposed_trade=proposed_trade,
                final_response=player_answer,
                final_resources=final_resources,
                player_outcome=outcome,
            ),
        )

        self.game_state.append(datum)
