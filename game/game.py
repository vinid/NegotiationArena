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
from game.utils import get_next_filename


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
        logging full game state
        """
        # log full state
        with open(os.path.join(self.log_path, "game_state.json"), "w") as f:
            json.dump(self.to_dict(), f, cls=GameEncoder, indent=2)

        self.log_human_readable_state()

    def log_human_readable_state(self):
        """
        easy to inspect log file
        """
        # log human-readable state
        settings = self.game_state[0]["settings"]

        # log meta information
        log_str = "Game Settings\n\n"
        for idx, player_settings in enumerate(
            zip(
                *[
                    [(k, str(p)) for p in v]
                    for k, v in settings.items()
                    if not (k == "iterations" or k == "resources_support_set")
                ]
            )
        ):
            log_str += "Player {} Settings:\n".format(idx + 1)
            log_str += "\n".join(
                ["\t{}: {}".format(_[0], _[1]) for _ in player_settings]
            )
            log_str += "\n\n"
        log_str += "------------------ \n"

        # log game state
        for state in self.game_state[1:]:
            # turn = state['turn']
            if state["current_iteration"] == "END":
                continue
            data = [
                "Current Iteration: {}".format(state["current_iteration"]),
                "Turn: {}".format(state["turn"]),
                *[
                    "{}: {}".format(k, v)
                    for k, v in {
                        **state["player_public_info_dict"],
                        **state["player_private_info_dict"],
                    }.items()
                ],
            ]
            log_str += "\n".join(data)
            log_str += "\n\n"

        # log game summary
        log_str += "------------------ \n"
        if self.game_state[-1]["current_iteration"] == "END":
            state = self.game_state[-1]
            data = [
                "Current Iteration: {}".format(state["current_iteration"]),
                "Turn: {}".format(state["turn"]),
                *["{}: {}".format(k, v) for k, v in state["summary"].items()],
            ]
            log_str += "\n".join(data)

        # write to log-file
        with open(os.path.join(self.log_path, "interaction.log"), "w") as f:
            f.write(log_str)

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
            # obj = constructor(**game_state_dict, **game_state_dict.['game_state'][0]['settings'])
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
        self.current_iteration = 1

    @abstractmethod
    def game_over(self):
        """
        game over logic based on game state
        """
        pass

    @abstractmethod
    def check_winner(self):
        pass

    def read_iteration_message(self, iteration):
        datum = self.game_state[iteration].get("player_public_answer_string", None)
        datum = {} if datum is None else datum
        return datum

    def write_game_state(
        self,
        players,
        response,
    ):
        # parse response
        agent_message = self.game_interface.parse(response)

        datum = dict(
            current_iteration=self.current_iteration,
            turn=self.turn,
            player_public_answer_string=agent_message.message_to_other_player(),
            player_public_info_dict=agent_message.public,
            player_private_info_dict=agent_message.secret,
            player_complete_answer=response,
            player_state=[player.get_state() for player in players],
        )

        self.game_state.append(datum)

    def set_game_state(self, game_state_dict):
        # set game time
        self.run_epoch_time_ms = game_state_dict["run_epoch_time_ms"]

        # set game state
        self.game_state = game_state_dict["game_state"]

        # update iteration and turn
        last_state = self.game_state[-1]
        self.turn = last_state["turn"]
        self.current_iteration = last_state["current_iteration"]

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

    def resume(self, iteration: int):
        # branch off current logfile
        self.log_path = os.path.join(
            self.log_dir, get_next_filename(self.run_epoch_time_ms, folder=self.log_dir)
        )
        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        if iteration > len(self.game_state):
            raise ValueError(
                "Invalid Iteration, Resume Iteration = ({}); Current Iteration = ({})".format(
                    iteration, self.iteration
                )
            )

        # resume iteration N means replay iteration N, which means load state from N-1
        self.current_iteration = iteration

        # if restart whole game, turn is set to 0
        self.turn = self.game_state[iteration]["turn"] if iteration > 0 else 0

        self.game_state = self.game_state[:iteration]
        # set player states
        self.players = [
            Agent.from_dict(player) for player in self.game_state[-1]["player_state"]
        ]

    def run(self):
        """

        Execute the game / Main game engine

        """

        # patrick said it was a good idea to do it this way
        self.log_state()
        # start with iteration = 1
        for iteration in range(self.current_iteration, self.iterations + 1):
            self.current_iteration = iteration

            # get game state from last iteration
            message = self.read_iteration_message(iteration - 1)

            # player to take a step/action based on current game state
            response = self.players[self.turn].step(message)
            # print(response)

            # update game state based on players and player response
            self.write_game_state(self.players, response)

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
