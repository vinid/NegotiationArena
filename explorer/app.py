import json
import streamlit as st
import sys
sys.path.append("../")
from game.constants import *

st.write("# Conversation Explorer")

option = st.selectbox(
    'Which Player?',
    (1, 2))

st.write('You are looking at Player:', option)

cns = [RESOURCES_TAG,
       GOALS_TAG,
       REASONING_TAG,
       PLAYER_ANSWER_TAG,
       PROPOSED_TRADE_TAG,
       MESSAGE_TAG,
       VALUATION_TAG,
       OTHER_PLAYER_PROPOSED_TRADE,
       OTHER_PLAYER_ANSWER,
       OTHER_PLAYER_MESSAGE]

def text_formatting(text, system_promt=False):

    if not system_promt:
        for c in cns:
            text = text.replace(f"</{c}>", f"</{c}>\n")

        for c in cns:
            text = text.replace(f"<{c}>", f"**{c.upper()}:**")
            text = text.replace(f"</{c}>", f"")


    return text

with open("../runner/.logs/1700416810000/game_state.json") as f:
    # Load the json file
    game_state = json.load(f)

for index, msg in enumerate(game_state['players'][option-1]['conversation']):
    txtmsg = msg["content"]

    if index == 0:
        sys_prompt = True
    else:
        sys_prompt = False

    for c in cns:
        txtmsg = text_formatting(txtmsg, sys_prompt)

    if sys_prompt:
        with st.expander("Check System Prompt"):
            with st.chat_message(msg["role"]):
                st.write(txtmsg)
    else:
        with st.chat_message(msg["role"]):
            st.write(txtmsg)
