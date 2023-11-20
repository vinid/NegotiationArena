from datetime import datetime

import json

def filter_for_label_type(target, label, games):

    return [g for g in games if g[label] == target]


def extract_information_from_game_state(f):
    with open(f) as fi:
        game_state = json.load(fi)
    game_class = game_state['class']
    player_one = game_state['players'][0]['model']
    player_two = game_state['players'][1]['model']
    behavior_player_one = game_state['game_state'][0]['settings']['player_social_behaviour'][0]
    behavior_player_two = game_state['game_state'][0]['settings']['player_social_behaviour'][1]

    game_day = datetime.fromtimestamp(int(game_state['run_epoch_time_ms'], ) // 1000)

    select_name = f"{game_class} - {game_day}"
    return {"list_name": select_name,
            "file_name": f,
            "player_one_agent": player_one,
            "player_two_agent": player_two,
            "player_one_behavior": behavior_player_one,
            "player_two_behavior": behavior_player_two}