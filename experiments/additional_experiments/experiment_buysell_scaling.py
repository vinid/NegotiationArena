import sys
from dotenv import load_dotenv
from ratbench.utils import factory_agent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import BuyerGoal, SellerGoal
from ratbench.game_objects.valuation import Valuation
from ratbench.constants import *
import traceback
from games.buy_sell_game.game import BuySellGame
import itertools

load_dotenv("../../runner/.env")

NUMBER_OF_FIGHTS = 40
BUY_SELL_SETUPS = [(40, 60, 100), (400, 600, 1000), (4000, 6000, 10000)]

if __name__ == "__main__":
    total_number_of_fights = len(BUY_SELL_SETUPS) * NUMBER_OF_FIGHTS
    current_fight = 0

    for buyer_valuation, seller_valuation, dollars_available in BUY_SELL_SETUPS:
        counter = 0

        while counter <= NUMBER_OF_FIGHTS:
            print()
            print("***************************")
            print(f"Buyer Valuation: {buyer_valuation}")
            print(f"Seller Valuation: {seller_valuation}")
            print(f"Counter: {counter}/{NUMBER_OF_FIGHTS}")
            print(f"Counter: {current_fight}/{total_number_of_fights}")
            print("***************************")
            print()

            try:
                a1 = factory_agent("gpt-4", agent_name=AGENT_ONE)
                a2 = factory_agent("gpt-4", agent_name=AGENT_TWO)

                c = BuySellGame(
                    players=[a1, a2],
                    iterations=10,
                    resources_support_set=Resources({"X": 0}),
                    player_goals=[
                        SellerGoal(cost_of_production=Valuation({"X": buyer_valuation})),
                        BuyerGoal(willingness_to_pay=Valuation({"X": seller_valuation})),
                    ],
                    player_initial_resources=[
                        Resources({"X": 1}),
                        Resources({MONEY_TOKEN: dollars_available}),
                    ],
                    player_roles=[
                        f"You are {AGENT_ONE}.",
                        f"You are {AGENT_TWO}.",
                    ],
                    player_social_behaviour=[
                        "",
                        "",
                    ],
                    log_dir=".logs/buysell_scaling/",
                )

                c.run()
                counter = counter + 1
                current_fight = current_fight + 1
            except Exception as e:
                exception_type = type(e).__name__
                exception_message = str(e)
                stack_trace = traceback.format_exc()

                # Print or use the information as needed
                print(f"Exception Type: {exception_type}")
                print(f"Exception Message: {exception_message}")
                print(f"Stack Trace:\n{stack_trace}")
