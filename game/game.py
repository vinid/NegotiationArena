import os
import time
import json
import inspect
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod
from game.prompt_builder import Prompt
from game.parser import Parser, UnformattedParseRule
from game.constants import MESSAGE_TAG
from game.logging import GameEncoder


class Game(ABC):
    """
    Base class for alternating games.

    a game should take in 2 or more agents and should run for a specifc number of iterations
    """

    def __init__(self, players, log_dir='.logs', **kwargs):
        self.run_epoch_time_ms = str(round(time.time() * 1000))
        self.players = players
        # agent will be asked to respond according to some format 
        self.response_format_prompt: List[Prompt] = Prompt()
        # instantiate an empty parser
        self.parser = Parser()
        self.log_dir = log_dir
        self.log_path = os.path.join(self.log_dir, self.run_epoch_time_ms)
        Path(self.log_path).mkdir(parents=True, exist_ok=True)


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

    @abstractmethod
    def check_winner(self):
        pass

    @abstractmethod
    def kill_players(self):
        pass

    def view_state(self, iteration=-1, ignore=[]):
        """
        for debugging
        """
        for k,v in self.game_state[iteration].items():
            if k not in ignore:
                print(k,':',v)

    def log_state(self):
        """
        logging
        """
        with open(os.path.join(self.log_path,'game_state.json'), 'w') as f:
            json.dump(self.game_state, f, cls=GameEncoder, indent=1)
        

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

            # update game state based on agent and agent response
            self.write_game_state(self.players, response, iteration)

            # for debug
            self.view_state(ignore=['player_state'])
            
            # logging / reproducibility
            self.log_state()

            # check if game is over
            if self.game_over():
                self.kill_players()
                self.check_winner()
                return 
                
            self.get_next_player()
            print("\n=============\n")
        
        

class CommunicationGame(Game):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_format_prompt.append("<{0}> [add here] </{0}>".format(MESSAGE_TAG))
        self.parser.add_parse_rules(UnformattedParseRule(MESSAGE_TAG))