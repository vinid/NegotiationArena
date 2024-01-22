from abc import ABC, abstractmethod
from negobench.utils import from_name_and_tag_to_message

class AgentMessage:
    """
    Structured format for agent messages.
    Should define what agents can see of each other messages.
    """

    def __init__(self):
        self.public = {}
        self.secret = {}

    def add_public(self, key, message, tag_for_other_player=None):
        """

        :param key:
        :param message:
        :param tag_for_other_player: this is the tag that will be used to show the message to the other player. If None, the key will be used
        :return:
        """
        if tag_for_other_player is None:
            tag_for_other_player = key
        self.public[key] = {"content": message, "tag_for_other_player": tag_for_other_player}

    def add_secret(self, key, message):
        self.secret[key] = message

    def message_to_other_player(self):
        response = []
        for key, value in self.public.items():
            response.append(from_name_and_tag_to_message(value["tag_for_other_player"], value["content"]))

        r = "\n".join(response)

        return r

