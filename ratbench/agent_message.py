from abc import ABC, abstractmethod
class AgentMessageInterface:
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

    @abstractmethod
    def message_to_other_player(self):
        raise NotImplementedError

