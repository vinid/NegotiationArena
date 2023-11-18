import os
import time
import json
import copy
import inspect
from pathlib import Path
from typing import List
from abc import ABC, abstractmethod, abstractproperty
from game.constants import MESSAGE_TAG
from game.logging import GameEncoder
from game.interface import GameInterface
from game.agents.agents import Agent


class Game(ABC):
    """
    Base class for games.

    A game should take in :
    (1) players: players of the game as a list of agents
    (2) game_interface: interface specifiying game rules (as prompt) and communication interface (as a parser)


    """

    def __init__(
        self,
        players: List[List],
        game_interface: GameInterface,
        log_dir=".logs",
        log_path=None,
        **kwargs,
    ):
        self.run_epoch_time_ms = str(round(time.time() * 1000))

        self.players = players
        self.game_interface = game_interface
        self.game_state = None

        # logging
        self.log_dir = log_dir
        self.log_path = (
            os.path.join(self.log_dir, self.run_epoch_time_ms)
            if log_path is None
            else log_path
        )

        Path(self.log_path).mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def set_game_state(self, game_state_dict):
        pass

    def to_dict(self):
        return {"class": self.__class__.__name__, **copy.deepcopy(self.__dict__)}

    def log_state(self):
        """
        logging
        """
        # log full state
        with open(os.path.join(self.log_path, "game_state.json"), "w") as f:
            json.dump(self.to_dict(), f, cls=GameEncoder, indent=2)

    @classmethod
    def from_dict(cls, game_state_dict):
        game_state_dict = copy.deepcopy(game_state_dict)
        class_name = game_state_dict.pop("class")
        subclasses = cls.get_all_subclasses()
        constructor = (
            cls
            if class_name == cls.__name__
            else next((sub for sub in subclasses if sub.__name__ == class_name), None)
        )
        if constructor:
            # intialize game interface object
            game_state_dict["game_interface"] = GameInterface.from_dict(
                game_state_dict["game_interface"]
            )
            # initialize players
            game_state_dict["players"] = [
                Agent.from_dict(player) for player in game_state_dict["players"]
            ]
            obj = constructor(**game_state_dict)

            obj.set_game_state(game_state_dict)
            return obj
        else:
            raise ValueError(f"Unknown subclass: {class_name}")

    @classmethod
    def get_all_subclasses(cls):
        subclasses_set = set()
        # Recursively get subclasses of subclasses
        for subclass in cls.__subclasses__():
            subclasses_set.add(subclass)
            subclasses_set.update(subclass.get_all_subclasses())

        return list(subclasses_set)


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
        # list of dict for simplicity
        self.game_state = []
        self.iterations = iterations

    def read_iteration_message(self, iteration):
        datum = self.game_state[iteration].get("player_public_answer_string", None)
        datum = {} if datum is None else datum
        return datum

    def write_game_state(self, players, response, iteration):
        # parse response
        agent_message = self.game_interface.parse(response)

        datum = dict(
            iteration=iteration,
            turn=self.turn,
            player_public_answer_string=agent_message.message_to_other_player(),
            player_public_info_dict=agent_message.public,
            player_private_info_dict=agent_message.secret,
            player_complete_answer=response,
            player_state=[player.get_state() for player in players],
        )

        self.game_state.append(datum)

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
