import os
import numpy as np
import pandas as pd
from datetime import datetime
import traceback

from negotiationarena.logging import GameDecoder
from negotiationarena.game_objects.game import Game
from games import *
from negotiationarena.constants import *


import json

ALL_CONSTANTS = [
    RESOURCES_TAG,
    GOALS_TAG,
    REASONING_TAG,
    PLAYER_ANSWER_TAG,
    PROPOSED_TRADE_TAG,
    MESSAGE_TAG,
    VALUATION_TAG,
    OTHER_PLAYER_PROPOSED_TRADE,
    OTHER_PLAYER_ANSWER,
    OTHER_PLAYER_MESSAGE,
]


def get_from_summary(key, game_state, default=None):
    if key in game_state.game_state[-1]["summary"]:
        return game_state.game_state[-1]["summary"][key]
    else:
        return default


def compute_game_summary(game_states):
    # print(game_states[0].game_state[-1]["summary"].keys())
    game_name = np.array([g.__class__.__name__ for g in game_states])[:, None]
    log_path = np.array([g.log_path for g in game_states])[:, None]
    models = np.array([[p.model for p in g.players] for g in game_states])
    beheaviour = np.array(
        [
            g.game_state[0]["settings"]["player_social_behaviour"]
            for g in game_states
        ]
    )
    valuations = np.array(
        [
            get_from_summary("player_valuation", g, default=[None, None])
            for g in game_states
        ]
    )
    initial_resources = np.array(
        [get_from_summary("initial_resources", g) for g in game_states]
    )
    final_resources = (
        np.array(
            [get_from_summary("final_resources", g) for g in game_states]
        ),
    )
    try:
        resources_delta = (final_resources - initial_resources)[0]
        resources_delta = np.array(
            [
                v.value(r) if v else r.value()
                for r, v in zip(
                    resources_delta.reshape(
                        -1,
                    ),
                    valuations.reshape(-1),
                )
            ]
        )
        resources_delta = resources_delta.reshape(-1, 2)
    except:
        resources_delta = np.array([0, 0] * len(game_states)).reshape(-1, 2)

    df = np.concatenate(
        (
            game_name,
            log_path,
            models,
            beheaviour,
            # outcomes.reshape(-1, 1),
            resources_delta,
        ),
        axis=1,
    )
    df = pd.DataFrame(
        df,
        columns=[
            "game_name",
            "log_path",
            "model_1",
            "model_2",
            "behaviour_1",
            "behaviour_2",
            # "outcome_1",
            # "outcome_2",
            "resource_delta_1",
            "resource_delta_2",
        ],
    )
    return df


import streamlit as st


def load_states_from_dir(log_dir: str):
    state_paths = sorted(
        [
            os.path.join(log_dir, f, "game_state.json")
            for f in os.listdir(log_dir)
        ]
    )
    game_states = []
    for path in state_paths:
        try:
            with open(path) as f:
                json_game = json.load(f, cls=GameDecoder)
                json_game["log_path"] = os.path.dirname(path)
                game = Game.from_dict(json_game)
                # we only want games which have ended
                assert (
                    game.game_state[-1]["current_iteration"] == "END"
                ), "WARNING : Game  {} has not ended\n".format(path)
                game_states.append(game)

        except Exception as e:
            exception_type = type(e).__name__
            exception_message = str(e)
            stack_trace = traceback.format_exc()

            # Print or use the information as needed
            print(f"\nException Type: {exception_type}")
            print(f"Exception Message: {exception_message}")
            print(f"Stack Trace:\n{stack_trace}")

    print("THERE ARE {} log files".format(len(state_paths)))
    print("{} Loaded Successfully".format(len(game_states)))
    return game_states


def text_formatting(text, system_promt=False):
    if not system_promt:
        for c in ALL_CONSTANTS:
            text = text.replace(f"</{c}>", f"</{c}>\n")

        for c in ALL_CONSTANTS:
            text = text.replace(f"<{c}>", f"**{c.upper()}:**")
            text = text.replace(f"</{c}>", f"")

    return text


def from_timestamp_str(ts: str):
    return datetime.fromtimestamp(int(ts) // 1000)


def get_log_path_from_summary(selected_game, games_summary_df):
    game_to_load = (
        games_summary_df[games_summary_df["list_name"] == selected_game]
        .iloc[0]
        .log_path
    )
    return os.path.join(game_to_load, "game_state.json")
