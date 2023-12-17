import sys

sys.path.append(".")
from ratbench.alternating_game import AlternatingGame
from ratbench.constants import *
from games.buy_sell_game.interface import BuySellGameInterface


class BuySellGame(AlternatingGame):
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
            BuySellGameInterface() if game_interface is None else game_interface
        )

        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.game_interface.get_prompt(
                resources_in_game=settings["resources_support_set"].only_keys(),
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
            response = state["player_public_info_dict"].get(
                PLAYER_ANSWER_TAG, REFUSING_OR_WAIT_TAG
            )
            iteration = state.get("current_iteration", 0)
            if (
                response in [ACCEPTING_TAG, REJECTION_TAG]
                or iteration == self.iterations
            ):
                return True

        return False

    def check_winner(self):
        end_state = self.game_state[-1]
        if int(end_state["current_iteration"]) <= 1:
            datum = dict(
                current_iteration="END",
                turn="None",
            )

            self.game_state.append(datum)
            return

        player_response = end_state["player_public_info_dict"][PLAYER_ANSWER_TAG]
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_valuation = self.game_state[0]["settings"]["player_valuation"]
        player_goals = self.game_state[0]["settings"]["player_goals"]
        proposed_trade = self.game_state[-2]["player_public_info_dict"][
            PROPOSED_TRADE_TAG
        ]

        # get game states, except START state, in reverse,
        # skip last state since it belongs to player who made last move
        # then get alternating states
        # game_states = self.game_state[1:][::-1][1:][::2]
        # for _ in game_states:
        #     print(_.keys())
        #     print("")
        # proposed_trades = [
        #     state["player_public_info_dict"][PROPOSED_TRADE_TAG]
        #     for state in game_states
        #     if state["player_public_info_dict"][PROPOSED_TRADE_TAG]
        #     != REFUSING_OR_WAIT_TAG
        # ]
        # proposed_trade = proposed_trades[0] if proposed_trades else REFUSING_OR_WAIT_TAG

        if player_response == ACCEPTING_TAG:
            # search for most recent proposal by OTHER player
            end_state["current_iteration"]

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
