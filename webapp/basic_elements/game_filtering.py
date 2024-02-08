import streamlit as st


def game_filter(games_summary_df):
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
            games_summary_df[
                games_summary_df["behaviour_1"] == filter_behaviour_one
            ]
            if filter_behaviour_one
            else games_summary_df
        )
        games_summary_df = (
            games_summary_df[
                games_summary_df["behaviour_2"] == filter_behaviour_two
            ]
            if filter_behaviour_two
            else games_summary_df
        )
        return games_summary_df
