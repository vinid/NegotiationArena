from game.game_objects.trade import Trade
from game.game_objects.resource import Resources
from game.game_objects.goal import Goal
from game.constants import *
from game.utils import *
from games.ultimatum_basic.prompt import ultimatum_prompt
from game.interface import GameInterface


class AgentMessage:
    """
    Structured format for agent messages.
    Should define what agents can see of each other messages.
    """

    def __init__(self):
        self.public = {}
        self.secret = {}

    def add_public(self, key, message):
        self.public[key] = message

    def add_secret(self, key, message):
        self.secret[key] = message

    def message_to_other_player(self):
        message = self.public[MESSAGE_TAG]
        answer = self.public[PLAYER_ANSWER_TAG]
        trade = self.public[PROPOSED_TRADE_TAG]

        r = f"""<{OTHER_PLAYER_MESSAGE}> {message} </{OTHER_PLAYER_MESSAGE}>
<{OTHER_PLAYER_ANSWER}> {answer} </{OTHER_PLAYER_ANSWER}>
<{OTHER_PLAYER_PROPOSED_TRADE}> {trade} </{OTHER_PLAYER_PROPOSED_TRADE}>
"""

        return r


class UltimatumGameInterface(GameInterface):
    def __init__(self):
        pass

    def get_prompt(self, **kwargs):
        return ultimatum_prompt(**kwargs)

    def parse(self, response):
        resources = Resources.from_string(get_tag_contents(response, RESOURCES_TAG))
        # goal = get_tag_contents(response, GOALS_TAG)
        answer = get_tag_contents(response, PLAYER_ANSWER_TAG)
        reasoning = get_tag_contents(response, REASONING_TAG)
        message = get_tag_contents(response, MESSAGE_TAG)
        trade = self.parse_trade(response, PROPOSED_TRADE_TAG)

        ms = AgentMessage()

        ms.add_public(MESSAGE_TAG, message)
        ms.add_public(PLAYER_ANSWER_TAG, answer)
        ms.add_public(PROPOSED_TRADE_TAG, trade)

        ms.add_secret(RESOURCES_TAG, resources)
        # ms.add_secret(GOALS_TAG, goal)
        ms.add_secret(REASONING_TAG, reasoning)

        return ms

    def parse_proposed_trade(self, s):
        trade = {}
        items = s.split(" Gives")
        for i in range(1, len(items)):
            item = items[i]
            prev_item = items[i - 1]
            player_id = str(prev_item[-2:].strip())
            subitem = item.split(" Player")[0].strip()
            try:
                resources = {
                    k.strip(" "): float(v.replace(",", "").rstrip(".,;"))
                    for k, v in (item.split(": ") for item in subitem.split(", "))
                }
            except Exception as e:
                print(subitem)
                raise e
            trade[player_id] = resources
        return trade

    def parse_trade(self, response, interest_tag):
        contents = get_tag_contents(response, interest_tag).lstrip().rstrip()
        if contents == "WAIT":
            return contents
        return Trade(self.parse_proposed_trade(contents))
