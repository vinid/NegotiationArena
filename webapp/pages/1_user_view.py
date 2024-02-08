import sys

sys.path.append("../")
sys.path.append(".")


import os
import json
from glob import glob
from utils import *
import streamlit as st
from negotiationarena.constants import *
from webapp.basic_elements.game_filtering import *
from games import *

# data loading
root_dir = os.path.abspath(__file__).split("/")[:-3]
log_dir = st.text_input(
    "Log Directory", value=os.path.join("/", *root_dir, ".logs", "buysell")
)
log_files = glob(os.path.join(log_dir, "*", "*.json"))
games = load_states_from_dir(log_dir)
games_summary_df = compute_game_summary(games)
games_summary_df["list_name"] = games_summary_df[
    ["game_name", "log_path"]
].apply(
    lambda row: f"{row.game_name} - {from_timestamp_str(os.path.basename(row.log_path))}",
    axis=1,
)
print(games_summary_df)


# main page

st.write("# Conversation Explorer")

if games:
    # Selection Element
    games_summary_df = game_filter(games_summary_df)

    selected_game = st.selectbox(
        "Which Game?", list(games_summary_df["list_name"])
    )
    option = st.selectbox("Which Player?", (1, 2))

    game_to_load = get_log_path_from_summary(selected_game, games_summary_df)

    with open(game_to_load) as f:
        # Load the json file
        game_state = json.load(f)

    st.write("You are looking at Player:", option)
    for index, msg in enumerate(
        game_state["players"][option - 1]["conversation"]
    ):
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
