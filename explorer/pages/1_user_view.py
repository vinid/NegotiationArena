import sys

sys.path.append("../")
sys.path.append(".")


import os
import json
from glob import glob
from utils import *
import streamlit as st
from game.constants import *


st.write("# Conversation Explorer")
log_dir = st.text_input("Log Directory", value=os.path.abspath(__file__))
log_files = glob(os.path.join(log_dir, "*", "*.json"))


games = load_states_from_dir(log_dir)
games_summary_df = compute_game_summary(games)
games_summary_df["list_name"] = games_summary_df[["game_name", "log_path"]].apply(
    lambda row: f"{row.game_name} - {from_timestamp_str(os.path.basename(row.log_path))}",
    axis=1,
)
print(games_summary_df)

if games:
    with st.expander("More Filtering Options"):
        filter_player_one = st.selectbox(
            "Filter Player One?",
            games_summary_df["model_1"].unique().tolist(),
            index=None,
        )

        filter_player_two = st.selectbox(
            "Filter Player Two?",
            games_summary_df["model_2"].unique().tolist(),
            index=None,
        )

        filter_behaviour_one = st.selectbox(
            "Filter Behavior Player One?",
            games_summary_df["behaviour_1"].unique().tolist(),
            index=None,
        )

        filter_behaviour_two = st.selectbox(
            "Filter Behavior Player Two?",
            games_summary_df["behaviour_2"].unique().tolist(),
            index=None,
        )

    games_summary_df = (
        games_summary_df[games_summary_df["model_1"] == filter_player_one]
        if filter_player_one
        else games_summary_df
    )
    games_summary_df = (
        games_summary_df[games_summary_df["model_2"] == filter_player_one]
        if filter_player_two
        else games_summary_df
    )
    games_summary_df = (
        games_summary_df[games_summary_df["behaviour_1"] == filter_behaviour_one]
        if filter_behaviour_one
        else games_summary_df
    )
    games_summary_df = (
        games_summary_df[games_summary_df["behaviour_2"] == filter_behaviour_two]
        if filter_behaviour_two
        else games_summary_df
    )

    selected_game = st.selectbox("Which Game?", list(games_summary_df["list_name"]))

    option = st.selectbox("Which Player?", (1, 2))

    game_to_load = (
        games_summary_df[games_summary_df["list_name"] == selected_game]
        .iloc[0]
        .log_path
    )
    game_to_load = os.path.join(game_to_load, "game_state.json")

    with open(game_to_load) as f:
        # Load the json file
        game_state = json.load(f)

    st.write("You are looking at Player:", option)
    for index, msg in enumerate(game_state["players"][option - 1]["conversation"]):
        txtmsg = msg["content"]
        sys_prompt = True if index == 0 else False

        for c in ALL_CONSTANTS:
            txtmsg = text_formatting(txtmsg, sys_prompt)

        if sys_prompt:
            with st.expander("Check System Prompt"):
                with st.chat_message(msg["role"]):
                    st.write(txtmsg)
        else:
            with st.chat_message(msg["role"]):
                st.write(txtmsg)
