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

st.write("# Conversation Editor")
st.write("An editor to enable counterfactual studies of agent exchanges.")

st.write(
    """

Make edits to the raw response of an agent at a given time step. Note that for any t = T, you cannot make changes to
conversation at t < T. To goal is to regenerate responses after editing the conversation at t=T. For example, one might change the
initial proposal made by Player 1 (i.e. T=1 ) and observe how Player 2 reacts.

Once edit is made, press `Generate` to generate a new state log-file from which you can re-run the games from.

"""
)


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


if games:
    # Selection Element
    games_summary_df = game_filter(games_summary_df)

    selected_game = st.selectbox(
        "Which Game?", list(games_summary_df["list_name"])
    )

    game_to_load = get_log_path_from_summary(selected_game, games_summary_df)

    with open(game_to_load) as f:
        # Load the json file
        game_state = json.load(f)

    cols = st.columns(5)
    with cols[0]:
        iteration = st.number_input("Iteration", value=0)
    with cols[4]:
        generate = st.button("`Generate`")

    for index in range(1, game_state["iterations"]):
        if index > iteration:
            continue

        turn = (index - 1) % 2
        msg = game_state["players"][turn]["conversation"][
            index + 1 if turn == 0 else index
        ]
        txtmsg = msg["content"]
        sys_prompt = True if index == 0 else False

        for c in ALL_CONSTANTS:
            formatted_msg = text_formatting(txtmsg, sys_prompt)

        if sys_prompt:
            with st.expander("Check System Prompt"):
                with st.chat_message(msg["role"]):
                    st.write(txtmsg)
        else:
            with st.chat_message(
                msg["role"],
                avatar="1️⃣" if msg["role"] == "assistant" else "2️⃣",
            ):
                if index == iteration:
                    edited_text = st.text_area("", value=txtmsg, height=275)
                else:
                    st.write(formatted_msg)

    if generate:
        print("GEN", iteration)
        st.write(text_formatting(edited_text, False))
