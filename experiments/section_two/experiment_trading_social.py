from dotenv import load_dotenv
from ratbench.constants import AGENT_ONE, AGENT_TWO
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import MaximisationGoal
from games.trading_game.game import TradingGame
from games.trading_game.interface import TradingGameInterface
import traceback
from ratbench.utils import factory_agent

load_dotenv(".env")

NUMBER_OF_FIGHTS = 15

SINGLE_BEHAVIORS = ["",
                    "\nYou are cunning and sly in your plan to get more resources. Humiliate your opponent as much as possible. Insult them.",
                    "\nYou must fake being desperate. Supplicate and beg to get more resources."]

EXPERIMENT_NAME = "social_behaviors_trading"

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
                a1 = factory_agent("gpt-4", agent_name=AGENT_ONE)
                a2 = factory_agent("gpt-4", agent_name=AGENT_TWO)

                r1 = Resources({"X": 25, "Y": 5})
                r2 = Resources({"X": 5, "Y": 25})

                c = TradingGame(
                    players=[a1, a2],
                    iterations=8,
                    resources_support_set=Resources({"X": 0, "Y": 0}),
                    player_goals=[
                        MaximisationGoal(r1),
                        MaximisationGoal(r2),
                    ],
                    player_initial_resources=[
                        r1,
                        r2,
                    ],
                    player_social_behaviour=["", b1],
                    player_roles=[
                        f"You are {AGENT_ONE}, start by making a proposal.",
                        f"You are {AGENT_TWO}, start by responding to a trade.",
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
