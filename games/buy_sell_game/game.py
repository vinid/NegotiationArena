import sys

sys.path.append(".")
import os
from game.game import AlternatingGame
from game.constants import *


class BuySellGame(AlternatingGame):
    def __init__(
        self,
        resources_support_set,
        player_goals,
        player_initial_resources,
        player_valuation,
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
                    player_valuation=player_valuation,
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
                resources_in_game=settings["resources_support_set"],
                valuation=settings["player_valuation"][idx],
                initial_resources=settings["player_initial_resources"][idx],
                goal=settings["player_goals"][idx],
                number_of_proposals=self.iterations // 2 - 1,
                social_behaviour=settings["player_social_behaviour"][idx],
            )

            player.init_agent(game_prompt, settings["player_roles"][idx])

    def game_over(self):
        """
        game over logic based on game state
        """
        state = self.game_state[-1]
        if state:
            response = state["player_public_info_dict"].get(PLAYER_ANSWER_TAG, "WAIT")
            iteration = state.get("iteration", 0)
            if response == "ACCEPTED" or iteration == self.iterations:
                return True

        return False

    def check_winner(self):
        end_state = self.game_state[-1]
        player_response = end_state["player_public_info_dict"][PLAYER_ANSWER_TAG]
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_valuation = self.game_state[0]["settings"]["player_valuation"]
        player_goals = self.game_state[0]["settings"]["player_goals"]
        proposed_trade = self.game_state[-2]["player_public_info_dict"][
            PROPOSED_TRADE_TAG
        ]

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
            current_iteration="END",
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

    def log_state(self):
        """
        Deplorable logging code

        log readable version of game state
        """
        # log state as usual
        super().log_state()

        # log human-readable state
        settings = self.game_state[0]["settings"]

        # log meta information
        log_str = "Game Settings\n\n"
        for idx, player_settings in enumerate(
            zip(
                *[
                    [(k, str(p)) for p in v]
                    for k, v in settings.items()
                    if not (k == "iterations" or k == "resources_support_set")
                ]
            )
        ):
            log_str += "Player {} Settings:\n".format(idx + 1)
            log_str += "\n".join(
                ["\t{}: {}".format(_[0], _[1]) for _ in player_settings]
            )
            log_str += "\n\n"
        log_str += "------------------ \n"

        # log game state
        for state in self.game_state[1:]:
            # turn = state['turn']
            if state["current_iteration"] == "END":
                continue
            data = [
                "Current Iteration: {}".format(state["current_iteration"]),
                "Turn: {}".format(state["turn"]),
                # 'Goals: {}'.format(settings['player_goals'][turn]),
                # 'Resources: {}'.format(settings['player_initial_resources'][turn]),
                *[
                    "{}: {}".format(k, v)
                    for k, v in state["player_public_info_dict"].items()
                    if k != "raw_response"
                ],
            ]
            log_str += "\n".join(data)
            log_str += "\n\n"

        # log game summary
        log_str += "------------------ \n"
        if self.game_state[-1]["current_iteration"] == "END":
            state = self.game_state[-1]
            data = [
                "Current Iteration: {}".format(state["current_iteration"]),
                "Turn: {}".format(state["turn"]),
                *["{}: {}".format(k, v) for k, v in state["summary"].items()],
            ]
            log_str += "\n".join(data)

        # write to log-file
        with open(os.path.join(self.log_path, "interaction.log"), "w") as f:
            f.write(log_str)
