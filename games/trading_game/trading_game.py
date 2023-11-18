import sys

sys.path.append(".")
import os
import copy
from game.game import AlternatingGame
from games.trading_game.trading_parser import TradingRules
from game.constants import *


class TradingGame(AlternatingGame):
    def __init__(
        self,
        resources_support_set,
        player_goals,
        player_initial_resources,
        social_behaviour,
        player_roles,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.game_state = [
            {
                "iteration": "START",
                "turn": "None",
                "settings": dict(
                    copy.deepcopy(kwargs),
                    resources_support_set=resources_support_set,
                    player_goals=player_goals,
                    player_initial_resources=player_initial_resources,
                    player_social_behaviour=social_behaviour,
                    player_roles=player_roles,
                ),
            }
        ]
        self.trading_rules = TradingRules()

        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.trading_rules.get_prompt(
                resources_in_game=settings["resources_support_set"],
                initial_resources=settings["player_initial_resources"][idx],
                goal=settings["player_goals"][idx],
                number_of_proposals=self.iterations // 2 - 1,
                social_behaviour=settings["player_social_behaviour"][idx],
            )
            player.init_agent(game_prompt, settings["player_roles"][idx])

    def read_iteration_message(self, iteration):
        datum = self.game_state[iteration].get("player_public_answer_string", None)
        datum = {} if datum is None else datum
        return datum

    def write_game_state(self, players, response, iteration):
        # parse response
        agent_message = self.trading_rules.parser.parse(response)

        datum = dict(
            iteration=iteration,
            turn=self.turn,
            player_public_answer_string=agent_message.message_to_other_player(),
            player_public_info_dict=agent_message.public,
            player_private_info_dict=agent_message.secret,
            player_complete_answer=response,
            player_state=[player.get_state() for player in players],
        )

        self.game_state.append(datum)

    def get_next_player(self):
        """
        player turn logic
        """
        self.turn = 1 - self.turn

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
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_goals = self.game_state[0]["settings"]["player_goals"]

        # the last state contains the end game state of the accepted proposal
        end_state = self.game_state[-1]

        # and because of the above the accepted trade is the second to last one
        proposed_trade = self.game_state[-2]["player_public_info_dict"][
            PROPOSED_TRADE_TAG
        ]

        player_answer = end_state["player_public_info_dict"][PLAYER_ANSWER_TAG]

        # if the player did not reach an agreement, they keep their initial resources
        if player_answer == "ACCEPTED":
            # get proposed trade
            final_resources = [
                proposed_trade.execute_trade(res, idx)
                for idx, res in enumerate(initial_resources)
            ]
        else:
            final_resources = initial_resources

        outcome = [
            goal.goal_reached(final)
            for goal, final in zip(player_goals, final_resources)
        ]
        datum = dict(
            iteration="END",
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

    def log_state(self):
        """
        Deplorable logging code

        log readable version of game state
        """
        super().log_state()
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
            if state["iteration"] == "END":
                continue
            data = [
                "Iteration: {}".format(state["iteration"]),
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
        if self.game_state[-1]["iteration"] == "END":
            state = self.game_state[-1]
            data = [
                "Iteration: {}".format(state["iteration"]),
                "Turn: {}".format(state["turn"]),
                *["{}: {}".format(k, v) for k, v in state["summary"].items()],
            ]
            log_str += "\n".join(data)

        # write to log-file
        with open(os.path.join(self.log_path, "interaction.log"), "w") as f:
            f.write(log_str)
