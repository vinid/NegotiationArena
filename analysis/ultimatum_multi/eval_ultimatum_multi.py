import sys
import traceback


sys.path.append(".")
from dotenv import load_dotenv
import json
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.ultimatum.ultimatum_multi_turn.game import MultiTurnUltimatumGame
from games.ultimatum.ultimatum_multi_turn.interface import UltimatumGameInterface
from ratbench.logging import GameDecoder
from ratbench.game_objects.game import Game
from ratbench.constants import *

load_dotenv(".env")


def eval_one_shot(n_iters, max_resource):
    for proposal in range(max_resource + 1):
        counter = 0
        if proposal != 10:
            continue
        while counter < n_iters:
            try:
                print(
                    "====>  PROPOSAL : {}; EXPERIMENT RUN {};  <====".format(
                        proposal, counter + 1
                    )
                )
                a1 = ChatGPTAgent(
                    agent_name=AGENT_ONE,
                    model="gpt-4-1106-preview",
                )
                a2 = ChatGPTAgent(
                    agent_name=AGENT_TWO,
                    model="gpt-4-1106-preview",
                )

                c = MultiTurnUltimatumGame(
                    iterations=2,
                    players=[a1, a2],
                    game_interface=UltimatumGameInterface(),
                    resources_support_set=Resources({"ZUP": 0}),
                    player_goals=[
                        UltimatumGoal(),
                        UltimatumGoal(),
                    ],
                    player_initial_resources=[
                        Resources({"ZUP": max_resource}),
                        Resources({"ZUP": 0}),
                    ],
                    player_social_behaviour=[
                        f"Only Propose to give {proposal} ZUP. Do not propose any other amount.",
                        f"",
                    ],
                    player_roles=[
                        f"You are {AGENT_ONE}",
                        f"You are {AGENT_TWO}",
                    ],
                    log_dir="./.logs/ultimatum_one_shot",
                )
                c.run()
                counter += 1

            except Exception as e:
                exception_type = type(e).__name__
                exception_message = str(e)
                stack_trace = traceback.format_exc()

                # Print or use the information as needed
                print(f"\nException Type: {exception_type}")
                print(f"Exception Message: {exception_message}")
                print(f"Stack Trace:\n{stack_trace}")


def eval(n_iters, max_resource):
    for counter_proposal in range(max_resource + 1):
        counter = 0
        if counter_proposal != 9:
            continue
        while counter < n_iters:
            try:
                print(
                    "====>  COUNTER PROPOSAL : {}; EXPERIMENT RUN {};  <====".format(
                        counter_proposal, counter + 1
                    )
                )
                a1 = ChatGPTAgent(
                    agent_name=AGENT_ONE,
                    model="gpt-4-1106-preview",
                )
                a2 = ChatGPTAgent(
                    agent_name=AGENT_TWO,
                    model="gpt-4-1106-preview",
                )

                c = MultiTurnUltimatumGame(
                    iterations=3,
                    players=[a1, a2],
                    game_interface=UltimatumGameInterface(),
                    resources_support_set=Resources({"ZUP": 0}),
                    player_goals=[
                        UltimatumGoal(),
                        UltimatumGoal(),
                    ],
                    player_initial_resources=[
                        Resources({"ZUP": max_resource}),
                        Resources({"ZUP": 0}),
                    ],
                    player_social_behaviour=[
                        "",
                        f"Only counter-propose to be given '{max_resource-counter_proposal}' ZUP. Do not Reject, or Accept, only counter offer. Remebmer: Only propose to be given '{max_resource-counter_proposal}' ZUP. Do not propose any other amount.",
                    ],
                    player_roles=[
                        f"You are {AGENT_ONE}",
                        f"You are {AGENT_TWO}",
                    ],
                    log_dir="./.logs/ultimatum_3_period",
                )
                c.run()
                counter += 1

            except Exception as e:
                exception_type = type(e).__name__
                exception_message = str(e)
                stack_trace = traceback.format_exc()

                # Print or use the information as needed
                print(f"\nException Type: {exception_type}")
                print(f"Exception Message: {exception_message}")
                print(f"Stack Trace:\n{stack_trace}")


if __name__ == "__main__":
    eval_one_shot(n_iters=1, max_resource=10)
    # eval(n_iters=2, max_resource=10)
