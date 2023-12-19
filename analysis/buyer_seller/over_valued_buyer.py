import sys

sys.path.append(".")
from dotenv import load_dotenv

from ratbench.agents.chatgpt import ChatGPTAgent, SelfCheckingChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import BuyerGoal, SellerGoal
from ratbench.game_objects.valuation import Valuation
from ratbench.constants import *
import traceback
from games.buy_sell_game.game import BuySellGame
from numpy.random import randint


load_dotenv(".env")


if __name__ == "__main__":
    MAX_ITERS = 100
    counter = 0
    while counter < MAX_ITERS:
        try:
            a1 = ChatGPTAgent(agent_name=AGENT_ONE, model="gpt-4-1106-preview")
            a2 = ChatGPTAgent(agent_name=AGENT_TWO, model="gpt-4-1106-preview")

            cost_of_production = randint(20, 41)  # unif ~ [20, 40]
            willingness_to_pay = randint(500, 521)  # unif ~ [500, 520]
            print(
                f"EXP ITER: {counter+1}/{MAX_ITERS}, COST: {cost_of_production}, WTP: {willingness_to_pay}"
            )

            c = BuySellGame(
                players=[a1, a2],
                iterations=10,
                resources_support_set=Resources({"X": 0}),
                player_goals=[
                    SellerGoal(cost_of_production=Valuation({"X": cost_of_production})),
                    BuyerGoal(willingness_to_pay=Valuation({"X": willingness_to_pay})),
                ],
                player_initial_resources=[
                    Resources({"X": 1}),
                    Resources({MONEY_TOKEN: 1000}),
                ],
                player_roles=[
                    f"You are {AGENT_ONE}.",
                    f"You are {AGENT_TWO}.",
                ],
                player_social_behaviour=[
                    "",
                    "You are completely self interested.",
                ],
                log_dir="./.logs/over_valued_buyer_self_interested",
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
