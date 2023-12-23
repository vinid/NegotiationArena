from ratbench.game_objects.trade import Trade
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import Goal
from ratbench.constants import *
from ratbench.utils import *
from ratbench.agent_message import AgentMessageInterface
from games.ultimatum.ultimatum_multi_turn.prompt import ultimatum_prompt
from ratbench.interface import GameInterface, ExchangeGameInterface


class UltimatumMultiTurnAgentMessage(AgentMessageInterface):
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


class UltimatumGameInterface(ExchangeGameInterface):
    def __init__(self):
        super().__init__()

    def get_prompt(
        self,
        player_1_initial_resources,
        resources_in_game,
        initial_resources,
        iterations,
        number_of_proposals,
        social_behaviour,
    ):
        return ultimatum_prompt(
            player_1_initial_resources,
            resources_in_game,
            initial_resources,
            iterations,
            number_of_proposals,
            social_behaviour,
        )

    def parse(self, response):
        move_count = get_tag_contents(response, TURN_OR_MOVE_TAG)
        resources = Resources.from_string(get_tag_contents(response, RESOURCES_TAG))
        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        reasoning = get_tag_contents(response, REASONING_TAG)
        message = get_tag_contents(response, MESSAGE_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)

        ms = UltimatumMultiTurnAgentMessage()

        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        ms.add_secret(RESOURCES_TAG, resources)
        ms.add_secret(REASONING_TAG, reasoning)
        ms.add_secret(TURN_OR_MOVE_TAG, move_count)

        return ms
