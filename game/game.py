import os
import time
import json
import inspect
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod, abstractproperty
from game.prompt_builder import Prompt, ResponseFormatPrompt
from game.parser import Parser, UnformattedParseRule, PassThroughParseRule
from game.constants import MESSAGE_TAG
from game.logging import GameEncoder


class Game(ABC):
    """
    Base class for games.

    a game should take in 2 or more agents.
    it should specficy how a player should respond (response_format_prompt) and
    consequently how the response should be interpreted (parser)

    """

    def __init__(self, players, log_dir=".logs", **kwargs):
        self.run_epoch_time_ms = str(round(time.time() * 1000))

        self.players = players

        # logging
        self.log_dir = log_dir
        self.log_path = os.path.join(self.log_dir, self.run_epoch_time_ms)
        Path(self.log_path).mkdir(parents=True, exist_ok=True)


class AlternatingGame(Game):
    """
    An alternating game is a game type whereby players take turns to make moves

    A game requires implementation of

    (1) rules (`game_prompt`): A textual description of the context, rules, and objectives of the game

    (2) Parser

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

    @abstractmethod
    def read_iteration_message(self):
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
    def check_winner(self):
        pass

    def get_next_player(self):
        """
        player turn logic
        """
        self.turn = 1 - self.turn

    def view_state(self, iteration=-1, ignore=[]):
        """
        for debugging
        """
        print("State:")
        for k, v in self.game_state[iteration].items():
            if k not in ignore:
                print(k, ":", v)

    def log_state(self):
        """
        logging
        """
        # log full state
        with open(os.path.join(self.log_path, "game_state.json"), "w") as f:
            json.dump(self.game_state, f, cls=GameEncoder, indent=2)

    def run(self):
        """

        Execute the game

        """

        # patrick said it was a good idea to do it this way
        self.log_state()
        # start with iteration = 1
        for iteration in range(1, self.iterations + 1):
            # get game state from last iteration
            message = self.read_iteration_message(iteration - 1)

            # player to take a step/action based on current game state
            response = self.players[self.turn].step(message)
            # print(response)

            # update game state based on players and player response
            self.write_game_state(self.players, response, iteration)

            # for debug
            self.view_state(
                ignore=[
                    "player_public_answer_string",
                    "player_public_info_dict",
                    "player_private_info_dict",
                    "player_state",
                ]
            )

            # for logging / reproducibility
            self.log_state()

            # check if game is over
            if self.game_over():
                self.check_winner()
                self.log_state()
                return

            self.get_next_player()
            print("=============\n")
