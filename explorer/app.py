import json
import streamlit as st
import sys
sys.path.append("../")
from glob import glob
from utils import *
from game.constants import *

st.write("# Conversation Explorer")


ALL_CONSTANTS = [RESOURCES_TAG,
       GOALS_TAG,
       REASONING_TAG,
       PLAYER_ANSWER_TAG,
       PROPOSED_TRADE_TAG,
       MESSAGE_TAG,
       VALUATION_TAG,
       OTHER_PLAYER_PROPOSED_TRADE,
       OTHER_PLAYER_ANSWER,
       OTHER_PLAYER_MESSAGE]


games = [extract_information_from_game_state(f) for f in glob("../runner/.logs/*/*.json")]
game_name2dict = {g["list_name"]: g for g in games}

player_one_types = list(set([g["player_one_agent"] for g in games]))
player_two_types = list(set([g["player_two_agent"] for g in games]))

player_one_behavior = list(set([g["player_one_behavior"] for g in games]))
player_two_behavior = list(set([g["player_two_behavior"] for g in games]))

with st.expander("More Filtering Options"):
    filter_player_one = st.selectbox(
        "Filter Player One?",
        player_one_types,
        index=None,
    )

    filter_player_two = st.selectbox(
        "Filter Player Two?",
        player_two_types,
        index=None,
    )

    filter_per_behavior_one = st.selectbox(
        "Filter Behavior Player One?",
        player_one_behavior,
        index=None,
    )

    filter_per_behavior_two = st.selectbox(
        "Filter Behavior Player Two?",
        player_two_behavior,
        index=None,
    )

if filter_player_one:
    games = filter_for_label_type(filter_player_one, "player_one_agent", games)

if filter_player_two:
    games = filter_for_label_type(filter_player_two, "player_two_agent", games)



if filter_per_behavior_one:
    games = filter_for_label_type(filter_per_behavior_one, "player_one_behavior", games)

if filter_per_behavior_two:
    games = filter_for_label_type(filter_per_behavior_two, "player_two_behavior", games)


game_name2dict = {g["list_name"]: g for g in games}


select_game = st.selectbox(
    'Which Game?',
    game_name2dict.keys())


option = st.selectbox(
    'Which Player?',
    (1, 2))

st.write('You are looking at Player:', option)


def text_formatting(text, system_promt=False):

    if not system_promt:
        for c in ALL_CONSTANTS:
            text = text.replace(f"</{c}>", f"</{c}>\n")

        for c in ALL_CONSTANTS:
            text = text.replace(f"<{c}>", f"**{c.upper()}:**")
            text = text.replace(f"</{c}>", f"")

    return text

game_to_load = game_name2dict[select_game]["file_name"]

with open(game_to_load) as f:
    # Load the json file
    game_state = json.load(f)

for index, msg in enumerate(game_state['players'][option-1]['conversation']):
    txtmsg = msg["content"]

    if index == 0:
        sys_prompt = True
    else:
        sys_prompt = False

    for c in ALL_CONSTANTS:
        txtmsg = text_formatting(txtmsg, sys_prompt)

    if sys_prompt:
        with st.expander("Check System Prompt"):
            with st.chat_message(msg["role"]):
                st.write(txtmsg)
    else:
        with st.chat_message(msg["role"]):
            st.write(txtmsg)
