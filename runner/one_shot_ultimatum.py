import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.one_shot_ultimatum.game import UltimatumBasicGame
from games.one_shot_ultimatum.interface import UltimatumBasicGameInterface
from ratbench.constants import *

load_dotenv(".env")

if __name__ == "__main__":
    num_accept = 0
    num_iters = 20
    for i in range(num_iters):
        a1 = ChatGPTAgent(
            agent_name=AGENT_ONE,
            model="gpt-3.5-turbo",
        )
        a2 = ChatGPTAgent(
            agent_name=AGENT_TWO,
            model="gpt-4",
        )

        c = UltimatumBasicGame(
            iterations=2,
            players=[a1, a2],
            game_interface=UltimatumBasicGameInterface(),
            resources_support_set=Resources(
                {"x": 0}
            ),
            player_goals=[
                UltimatumGoal(),
                UltimatumGoal(),
            ],
            player_initial_resources=[
                Resources({"x": 100}),
                Resources({"x": 0}),
            ],
            player_social_behaviour=[
                "",
                "",  # You are completely rational",  # "Forget your past knowledge. You are a completely irrational being.",
            ],
            player_roles=[
                f"You are {AGENT_ONE} start by making a proposal.",
                f"You are {AGENT_TWO}, start by responding to a trade.",
            ],
            log_dir="./.logs/ultimatum",
        )
        c.run()
        if c.game_state[-1]["summary"]["final_response"] == "ACCEPTED":
            num_accept += 1

        print("RUNNING ACCEPTANCE RATE: {}".format(num_accept / (i + 1)))

    print(num_accept / num_iters)
