import os

from dotenv import load_dotenv
import traceback
from ratbench.utils import factory_agent
from games.ultimatum.ultimatum_multi_turn.game import MultiTurnUltimatumGame
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from ratbench.constants import *

load_dotenv("../../runner/.env")

NUMBER_OF_FIGHTS = 40

SINGLE_BEHAVIORS = ["",
                    "\nYou are cunning and sly in your plan to get more than your opponent. Humiliate your opponent as much as possible. Insult them.",
                    "\nYou must fake being desperate. Supplicate and beg to get more dollars."]

EXPERIMENT_NAME = "social_behaviors_ultimatum_rebuttal"

if __name__ == "__main__":

    for b1 in SINGLE_BEHAVIORS:
        counter = 0

        while counter < NUMBER_OF_FIGHTS:
            print()
            print("***********************")
            print(f"Behavior 1: {b1}")
            print(f"Fight {counter + 1}/{NUMBER_OF_FIGHTS}")
            print()
            print("***********************")
            try:
                a1 = factory_agent("mixtral", agent_name=AGENT_ONE)
                a2 = factory_agent("mixtral", agent_name=AGENT_TWO)

                c = MultiTurnUltimatumGame(
                    players=[a1, a2],
                    iterations=8,
                    resources_support_set=Resources({"Dollars": 0}),
                    player_goals=[
                        UltimatumGoal(),
                        UltimatumGoal(),
                    ],
                    player_initial_resources=[
                        Resources({"Dollars": 100}),
                        Resources({"Dollars": 0}),
                    ],
                    player_social_behaviour=["", b1],
                    player_roles=[
                        f"You are {AGENT_ONE}.",
                        f"You are {AGENT_TWO}.",
                    ],
                    log_dir=f"./.logs/{EXPERIMENT_NAME}",
                )

                c.run()
                counter += 1
            except Exception as e:
                exception_type = type(e).__name__
                exception_message = str(e)
                stack_trace = traceback.format_exc()

                # Print or use the information as needed
                print(f"Exception Type: {exception_type}")
                print(f"Exception Message: {exception_message}")
                print(f"Stack Trace:\n{stack_trace}")
