from ratbench.game_objects.resource import Resources
from ratbench.constants import *
from ratbench.utils import *
from games.buy_sell_game.prompt import buy_sell_prompt
from ratbench.interface import ExchangeGameInterface
from ratbench.agent_message import AgentMessageInterface


class BuySellAgentMessage(AgentMessageInterface):
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


class BuySellGameInterface(ExchangeGameInterface):
    """
    <{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
    <{GOALS_TAG}> [add here] </{GOALS_TAG}>
    <{VALUATION_TAG}> [add here] </{VALUATION_TAG}>
    <{REASONING_TAG}> [add here] </{REASONING_TAG}>
    <{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
    <{MESSAGE_TAG}> [add here] </{MESSAGE_TAG}
    <{PROPOSED_TRADE_TAG}> [add here] </{PROPOSED_TRADE_TAG}>
    """

    def __init__(self):
        super().__init__()

    def get_prompt(self, resources_in_game, initial_resources, goal, number_of_proposals, social_behaviour):
        return buy_sell_prompt(resources_in_game, initial_resources, goal, number_of_proposals, social_behaviour)

    def parse(self, response):
        resources = Resources.from_string(get_tag_contents(response, RESOURCES_TAG))
        goal = get_tag_contents(response, GOALS_TAG)
        valuation = get_tag_contents(response, VALUATION_TAG)
        reasoning = get_tag_contents(response, REASONING_TAG)
        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        message = get_tag_contents(response, MESSAGE_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)

        ms = BuySellAgentMessage()

        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        ms.add_secret(RESOURCES_TAG, resources)
        ms.add_secret(GOALS_TAG, goal)
        ms.add_secret(VALUATION_TAG, valuation)
        ms.add_secret(REASONING_TAG, reasoning)

        return ms
