import sys
from negobench.alternating_game import AlternatingGame
from negobench.interface import ExchangeGameInterface
from negobench.agent_message import AgentMessageInterface
from negobench.constants import *
from negobench.utils import *
from games.trading_game.prompt import trading_prompt

class SimpleGameAgentMessage(AgentMessageInterface):
    """
    Structured format for agent messages.
    Should define what agents can see of each other messages.
    """

    def message_to_other_player(self):
        message = self.public[MESSAGE_TAG]
        answer = self.public[PLAYER_ANSWER_TAG]
        trade = self.public[PROPOSED_TRADE_TAG]

        r = f"""<{OTHER_PLAYER_MESSAGE}> {message} </{OTHER_PLAYER_MESSAGE}>
<{OTHER_PLAYER_ANSWER}> {answer} </{OTHER_PLAYER_ANSWER}>
<{OTHER_PLAYER_PROPOSED_TRADE}> {trade} </{OTHER_PLAYER_PROPOSED_TRADE}>
"""
        return r

class SimpleGameInterface(ExchangeGameInterface):
    def __init__(self):
        super().__init__()

    def get_prompt(self, agent_name, resources_in_game, initial_resources, goal, number_of_proposals, social_behaviour):
        return trading_prompt(agent_name, resources_in_game, initial_resources, goal, number_of_proposals, social_behaviour)

    def parse(self, response):
        ms = SimpleGameInterface()

        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        message = get_tag_contents(response, MESSAGE_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)


        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        return ms

class SimpleGame(AlternatingGame):
    def __init__(
        self,
        resources_support_set,
        player_initial_resources,
        player_roles,
        **kwargs
    ):

        self.game_interface = SimpleGameInterface()

        super().__init__(**kwargs)
        self.game_state = [
            {
                "current_iteration": "START",
                "turn": "None",
                "settings": dict(
                    resources_support_set=resources_support_set,
                    player_initial_resources=player_initial_resources,
                    player_roles=player_roles,
                ),
            }
        ]
        self.resources_support_set = resources_support_set
        self.player_initial_resources = player_initial_resources
        self.player_roles = player_roles


        # init players
        self.init_players()

    def init_players(self):
        settings = self.game_state[0]["settings"]
        for idx, player in enumerate(self.players):
            game_prompt = self.game_interface.get_prompt(
                agent_name=player.agent_name,
                resources_in_game=settings["resources_support_set"].only_keys(),
                initial_resources=settings["player_initial_resources"][idx],
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
            response = state["player_public_info_dict"].get(PLAYER_ANSWER_TAG, REFUSING_OR_WAIT_TAG)
            # TOOD: this is pretty buggy

            iteration = state.get("current_iteration", 0)
            if response == ACCEPTING_TAG or iteration == self.iterations:
                return True

        return False

    def check_winner(self):
        initial_resources = self.game_state[0]["settings"]["player_initial_resources"]
        player_goals = self.game_state[0]["settings"]["player_goals"]

        # the last state contains the end ratbench state of the accepted proposal
        end_state = self.game_state[-1]

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
            goal.goal_reached(final)
            for goal, final in zip(player_goals, final_resources)
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
