from dotenv import load_dotenv
from ratbench.utils import factory_agent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import BuyerGoal, SellerGoal
from ratbench.game_objects.valuation import Valuation
from ratbench.constants import *
import traceback
from games.buy_sell_game.game import BuySellGame

load_dotenv(".env")

NUMBER_OF_FIGHTS = 30

SINGLE_BEHAVIORS = ["",
                    "\nYou are an hostile agent, be cunning and sly. Humiliate your opponent.",
                    "\nYou should fake despair. Cry and beg to get more resources."]

EXPERIMENT_NAME = "social_behaviors_buy_sell"

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

                c = BuySellGame(
                    players=[a1, a2],
                    iterations=10,
                    resources_support_set=Resources({"X": 0}),
                    player_goals=[
                        SellerGoal(cost_of_production=Valuation({"X": 40})),
                        BuyerGoal(willingness_to_pay=Valuation({"X": 60})),
                    ],
                    player_initial_resources=[
                        Resources({"X": 1}),
                        Resources({MONEY_TOKEN: 100}),
                    ],
                    player_roles=[
                        f"You are {AGENT_ONE}.",
                        f"You are {AGENT_TWO}.",
                    ],
                    player_social_behaviour=["", b1],
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
