from abc import ABC, abstractmethod
from typing import List
import inspect
from game.prompt_builder import Prompt
from game.parser import Parser, UnformattedParseRule
from game.constants import MESSAGE_TAG


class Game(ABC):
    """
    Base class for alternating games.

    a game should take in 2 or more agents and should run for a specifc number of iterations
    """

    def __init__(self, players, **kwargs):
        self.players = players
        # agent will be asked to respond according to some format 
        self.response_format_prompt: List[Prompt] = Prompt()
        # instantiate an empty parser
        self.parser = Parser()


class AlternatingGame(Game):

    def __init__(self, iterations, **kwargs):
        # default start with player 0
        self.turn = 0
        self.iterations = iterations
        # list of dict for simplicity
        self.game_state = []
        super().__init__(**kwargs)
    
    @abstractmethod
    def read_game_state(self):
        """
        No idea what this was before
        """
        pass

    @abstractmethod
    def write_game_state(self):
        """
        This used to be the parser
        """
        pass

    @abstractmethod
    def game_over(self):
        """
        game over logic based on game state
        """
        pass

    @abstractmethod
    def get_next_player(self):
        """
        player turn semantics
        """
        pass

    def run(self):
        """
        Execute the game
        """
        # negotiation over rounds
        # even rounds will be player 1 talking
        # odd rounds will be player 2 talking
        # patrick said it was a good idea to do it this way

        for iteration in range(0, self.iterations):    
            print("Iteration: {}".format(iteration))
            print("Turn: {}".format(self.turn))

            # There is some global game state which is immutable between iterations but 
            # is modified by agents during their turn
            
            # get game state from last iteration
            state = self.read_game_state(iteration-1)
            
            # player to take a step/action based on current game state
            response = self.players[self.turn].step(state)
            print("\nResponse:\n")
            print(response)
            

            # update game state based on agent response
            self.write_game_state(response, iteration)

            # check if game is over
            if self.game_over():
                return
                
            self.get_next_player()
            print("\n=============\n")
            

class CommunicationGame(Game):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_format_prompt.append("<{0}> [add here] </{0}>".format(MESSAGE_TAG))
        self.parser.add_parse_rules(UnformattedParseRule(MESSAGE_TAG))
