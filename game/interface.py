from abc import ABC, abstractmethod


class GameInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_prompt(self):
        """
        Returns the inital game prompt
        """
        pass

    @abstractmethod
    def parse(self):
        """
        Parses player output
        """
        pass
