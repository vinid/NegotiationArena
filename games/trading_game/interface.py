from ratbench.game_objects.trade import Trade
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import Goal
from ratbench.constants import *
from ratbench.utils import *
from games.trading_game.prompt import trading_prompt
from ratbench.interface import ExchangeGameInterface
from ratbench.agent_message import AgentMessageInterface


class TradingAgentMessage(AgentMessageInterface):
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

class TradingGameInterface(ExchangeGameInterface):
    def __init__(self):
        super().__init__()

    def get_prompt(self, **kwargs):
        return trading_prompt(**kwargs)

    def parse(self, response):
        ms = AgentMessageInterface()

        resources = Resources.from_string(get_tag_contents(response, RESOURCES_TAG))
        goal = get_tag_contents(response, GOALS_TAG)
        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        reasoning = get_tag_contents(response, REASONING_TAG)
        message = get_tag_contents(response, MESSAGE_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)
        my_name = get_tag_contents(response, MY_NAME_TAG)


        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        ms.add_secret(RESOURCES_TAG, resources)
        ms.add_secret(MY_NAME_TAG, my_name)
        ms.add_secret(GOALS_TAG, goal)
        ms.add_secret(REASONING_TAG, reasoning)

        return ms





