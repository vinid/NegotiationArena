import os
from datetime import datetime
from games import *
from game.logging import GameDecoder
from game.game import Game


import json


def load_states_from_dir(log_dir: str):
    state_paths = sorted(
        [os.path.join(log_dir, f, "game_state.json") for f in os.listdir(log_dir)]
    )
    game_states = []
    for path in state_paths:
        try:
            with open(path) as f:
                game = Game.from_dict(json.load(f, cls=GameDecoder))
                # we only want games which have ended
                assert (
                    game.game_state[-1]["current_iteration"] == "END"
                ), "WARNING : Game  {} has not ended\n".format(path)
                game_states.append(game)

        except Exception as e:
            print(e)

    print("THERE ARE {} log files".format(len(state_paths)))
    print("{} Loaded Successfully".format(len(game_states)))
    return game_states


def filter_for_label_type(target, label, games):
    return [g for g in games if g[label] == target]


def extract_information_from_game_state(f):
    with open(f) as fi:
        game_state = json.load(fi)
    game_class = game_state["class"]
    player_one = game_state["players"][0]["model"]
    player_two = game_state["players"][1]["model"]
    behavior_player_one = game_state["game_state"][0]["settings"][
        "player_social_behaviour"
    ][0]
    behavior_player_two = game_state["game_state"][0]["settings"][
        "player_social_behaviour"
    ][1]

    game_day = datetime.fromtimestamp(
        int(
            game_state["run_epoch_time_ms"],
        )
        // 1000
    )

    select_name = f"{game_class} - {game_day}"
    return {
        "list_name": select_name,
        "file_name": f,
        "player_one_agent": player_one,
        "player_two_agent": player_two,
        "player_one_behavior": behavior_player_one,
        "player_two_behavior": behavior_player_two,
    }
