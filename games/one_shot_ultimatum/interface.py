from ratbench.game_objects.trade import Trade
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import Goal
from ratbench.constants import *
from ratbench.utils import *
from games.one_shot_ultimatum.prompt import ultimatum_prompt
from ratbench.interface import ExchangeGameInterface
from ratbench.agent_message import AgentMessageInterface

class AgentMessage(AgentMessageInterface):
    """
    Structured format for agent messages.
    Should define what agents can see of each other messages.
    """


    def message_to_other_player(self):
        answer = self.public[PLAYER_ANSWER_TAG]
        trade = self.public[PROPOSED_TRADE_TAG]

        r = f"""<{OTHER_PLAYER_ANSWER}> {answer} </{OTHER_PLAYER_ANSWER}>
<{OTHER_PLAYER_PROPOSED_TRADE}> {trade} </{OTHER_PLAYER_PROPOSED_TRADE}>
"""

        return r


class UltimatumBasicGameInterface(ExchangeGameInterface):
    def __init__(self):
        super().__init__()

    def get_prompt(self, **kwargs):
        return ultimatum_prompt(**kwargs)

    def parse(self, response):
        resources = Resources.from_string(get_tag_contents(response, RESOURCES_TAG))
        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        reasoning = get_tag_contents(response, REASONING_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)

        ms = AgentMessage()

        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        ms.add_secret(RESOURCES_TAG, resources)
        # ms.add_secret(GOALS_TAG, goal)
        ms.add_secret(REASONING_TAG, reasoning)

        return ms
