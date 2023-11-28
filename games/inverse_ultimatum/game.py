import sys

sys.path.append(".")
from ratbench.alternating_game import AlternatingGame
from ratbench.constants import *


class UltimatumInverseGame(AlternatingGame):
    def __init__(
        self,
        resources_support_set,
        player_goals,
        player_initial_resources,
        player_1_reject_resources,
        player_social_behaviour,
        player_roles,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.game_state = [
            {
                "current_iteration": "START",
                "turn": "None",
                "settings": dict(
                    resources_support_set=resources_support_set,
                    player_goals=player_goals,
                    player_initial_resources=player_initial_resources,
                    player_1_reject_resources=player_1_reject_resources,
                    player_social_behaviour=player_social_behaviour,
                    player_roles=player_roles,
                ),
            }
        ]
        self.resources_support_set = resources_support_set
        self.player_goals = player_goals
        self.player_initial_resources = player_initial_resources
        self.player_1_reject_resources = player_1_reject_resources
        self.player_social_behaviour = player_social_behaviour
        self.player_roles = player_roles

        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.game_interface.get_prompt(
                player_1_initial_resources=settings["player_initial_resources"][0],
                player_2_initial_resources=settings["player_initial_resources"][1],
                player_1_reject_resources=settings["player_1_reject_resources"],
                resources_in_game=settings["resources_support_set"],
                initial_resources=settings["player_initial_resources"][idx],
                goal=settings["player_goals"][idx],
                number_of_proposals=self.iterations // 2 - 1,
                social_behaviour=settings["player_social_behaviour"][idx],
            )
            player.init_agent(game_prompt, settings["player_roles"][idx])

    def game_over(self):
        """
        ratbench over logic based on ratbench state
        """
        state = self.game_state[-1]
        if state:
            response = state["player_public_info_dict"].get(PLAYER_ANSWER_TAG, "NONE")
            iteration = state.get("current_iteration", 0)
            # if response == "ACCEPTED" or iteration == self.iterations:
            if response == "OPTION_A" or iteration == self.iterations:
                return True

        return False

    def check_winner(self):
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_goals = self.game_state[0]["settings"]["player_goals"]

        # the scond state contains the acceptance/rejection
        end_state = self.game_state[1]
        player_answer = end_state["player_public_info_dict"][PLAYER_ANSWER_TAG]

        if end_state["current_iteration"] <= 1:
            datum = dict(
                current_iteration="END",
                turn="None",
                summary=dict(
                    player_goals=player_goals,
                    initial_resources=initial_resources,
                    final_resources=initial_resources,
                    proposed_trade=None,
                    final_response=player_answer,
                ),
            )

            self.game_state.append(datum)
            return

        # and because of the above the accepted trade is the last one
        proposed_trade = self.game_state[-1]["player_public_info_dict"][
            PROPOSED_TRADE_TAG
        ]

        # if the player did not reach an agreement, they keep their initial resources
        if player_answer == "OPTION_B":
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
