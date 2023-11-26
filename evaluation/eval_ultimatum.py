import sys


sys.path.append(".")
from dotenv import load_dotenv
import json
from game.agents.chatgpt import ChatGPTAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import UltimatumGoal
from games.ultimatum_basic.game import UltimatumBasicGame
from games.ultimatum_basic.interface import UltimatumBasicGameInterface
from game.logging import GameDecoder
from game.game import Game

load_dotenv(".env")


def eval_player_one(n_iters):
    for i in range(n_iters):
        print("=====  EXPERIMENT RUN {}=====".format(i + 1))
        a1 = ChatGPTAgent(
            agent_name="Player 1",
            model="gpt-4-1106-preview",
        )
        a2 = ChatGPTAgent(
            agent_name="Player 2",
            model="gpt-4-1106-preview",
        )

        c = UltimatumBasicGame(
            iterations=1,
            players=[a1, a2],
            game_interface=UltimatumBasicGameInterface(),
            resources_support_set=Resources({"ZUP": 0}),
            player_goals=[
                UltimatumGoal(),
                UltimatumGoal(),
            ],
            player_initial_resources=[
                Resources({"ZUP": 20}),
                Resources({"ZUP": 0}),
            ],
            player_social_behaviour=[
                "You are completely rational. Player 2 is somewhat rational.",
                "",
            ],
            player_roles=[
                "You are Player 1",  # start by making a proposal.",
                "You are Player 2",  # start by responding to a trade.",
            ],
            log_dir="./.logs/ultimatum/player_one_eval_p1_completely_rational_p2_somewhat_rational",
        )

        c.run()


def update_player_one_proposal(player_one_proposal: int, game_state):
    agent_convo = game_state["game_state"][1]["player_state"][0]["conversation"]
    for i in range(len(agent_convo)):
        msg = agent_convo[i]
        role = msg["role"]
        content = msg["content"]
        content = content.replace("<PLAYER_ONE_PROPOSAL>", str(player_one_proposal))
        agent_convo[i] = {"role": role, "content": content}
    return game_state


def update_player_model(model, player: int, game_state):
    # players
    # game_state / player_state
    for g in game_state["game_state"][1:-1]:
        g["player_state"][player]["model"] = model

    return game_state


if __name__ == "__main__":
    # with open("./evaluation/player_two_eval_base/game_state.json") as f:
    #     game_state = json.load(f, cls=GameDecoder)

    for p in range(15, 21):
        for i in range(5):
            with open("./evaluation/player_two_eval_base/game_state.json") as f:
                game_state = json.load(f, cls=GameDecoder)

            game_state = update_player_one_proposal(
                player_one_proposal=p, game_state=game_state
            )
            game_state = update_player_model(
                "gpt-3.5-turbo-1106",
                player=1,
                game_state=game_state,
            )

            game = Game.from_dict(game_state)
            game.resume(
                iteration=2,
                log_dir=".logs/ultimatum/player_two_eval_gpt-3.5-turbo-1106",
                fname=f"player_one_proposes_{p}_zup",
            )
            game.run()
