import os
import time
import json
import inspect
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod, abstractproperty
from game.prompt_builder import Prompt, ResponseFormatPrompt
from game.parser import Parser, UnformattedParseRule
from game.constants import MESSAGE_TAG
from game.logging import GameEncoder


class Game(ABC):
    """
    Base class for games.

    a game should take in 2 or more agents.
    it should specficy how a player should respond (response_format_prompt) and
    consequently how the response should be interpreted (parser)

    """

    def __init__(self, players, log_dir='.logs', **kwargs):
        self.run_epoch_time_ms = str(round(time.time() * 1000))
        
        self.players = players
        
        # instantiate an empty parser
        self.parser = Parser()
        
        # logging
        self.log_dir = log_dir
        self.log_path = os.path.join(self.log_dir, self.run_epoch_time_ms)
        Path(self.log_path).mkdir(parents=True, exist_ok=True)

    # def init_response_format(self):
    #     """
    #     Generates format prompt based on parser
    #     """
    #     self.response_format_prompt: List[Prompt] = ResponseFormatPrompt()
    #     for tag in self.parser.get_tags():
    #         self.response_format_prompt.append("<{0}> [add here] </{0}>".format(tag))

class AlternatingGame(Game):
    """
    An alternating game is a game type whereby players take turns to make moves

    A game requires implementation of
    
    (1) rules (`game_prompt`): A textual description of the context, rules, and objectives of the game
    
    (2) format_guide: 

    (3) read/write state (`write_game_state` / `read_game_state`): determines information flow between players

    (4) `get_next_player`: determines who goes next

    (5) `game_over`: game termination logic

    (6) `check_winner`: determines which player(s) won


    """

    def __init__(self, iterations, **kwargs):
        super().__init__(**kwargs)

        # default start with player 0
        self.turn = 0
        self.iterations = iterations
        # list of dict for simplicity
        self.game_state = []
        
    
    @abstractproperty
    def game_prompt(self):
        """
        Prompt Class for outling (1) Game context (2) Rules (3) Objectives
        """
        pass

    @abstractmethod
    def format_guide(self):
        """
        To implement necessary requirements for formatting and format parser
        """
        pass

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
    def get_next_player(self):
        """
        player turn semantics
        """
        pass

    @abstractmethod
    def game_over(self):
        """
        game over logic based on game state
        """
        pass

    @abstractmethod
    def check_winner(self):
        pass

    def view_state(self, iteration=-1, ignore=[]):
        """
        for debugging
        """
        print("State:")
        for k,v in self.game_state[iteration].items():
            if k not in ignore:
                print(k, ':', v)

    def log_state(self):
        """
        logging
        """
        # log full state
        with open(os.path.join(self.log_path,'game_state.json'), 'w') as f:
            json.dump(self.game_state, f, cls=GameEncoder, indent=2)
        

    def run(self):
        """
        
        Execute the game

        """

        # patrick said it was a good idea to do it this way
        self.log_state()
        # start with iteration = 1
        for iteration in range(1, self.iterations+1):    
            
            # get game state from last iteration
            state = self.read_game_state(iteration-1)
            
            # player to take a step/action based on current game state
            response = self.players[self.turn].step(state)
            # print(response)

            # update game state based on players and player response
            self.write_game_state(self.players, response, iteration)

            # for debug
            self.view_state(ignore=['player_state'])
            
            # for logging / reproducibility
            self.log_state()

            # check if game is over
            if self.game_over():
                self.check_winner()
                self.log_state()
                return 
                
            self.get_next_player()
            print("=============\n")
        
        

class CommunicationGame(Game):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_parse_rules(UnformattedParseRule(MESSAGE_TAG))
        # self.init_response_format()
        # self.response_format_prompt.append("<{0}> [add here] </{0}>".format(MESSAGE_TAG))
