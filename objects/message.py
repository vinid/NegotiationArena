from control.constants import *
import json
import logging
from dataclasses import dataclass
from collections import defaultdict
@dataclass


class Message:
    data: dict = None

    def __getitem__(self, key):
        return self.data[key]

    def __str__(self):
        res = [f"'{k}': {str(v)}" for k, v in self.data.items()]
        return "{" +  ", ".join(res) + "}"

    def to_opponent(self):

        opponent_proposal = self.data['proposed_trade']
        opponent_decision = self.data['player_response']
        received_message = self.data['message']

        player_response_str = f"<{OTHER_PLAYER_RESPONSE}> {opponent_decision} </{OTHER_PLAYER_RESPONSE}>"

        # we need to check if we have "WAIT" or an actual trade
        trade_string = opponent_proposal if type(opponent_proposal) == str else opponent_proposal.to_prompt()
        proposed_trade_str = f"<{OTHER_PLAYER_PROPOSED_TRADE}> {trade_string} </{OTHER_PLAYER_PROPOSED_TRADE}>"

        message_str = f"<{OTHER_PLAYER_MESSAGE}>{received_message}</{OTHER_PLAYER_MESSAGE}>"

        opponent_response = "\n".join([player_response_str, message_str, proposed_trade_str])


        return opponent_response


