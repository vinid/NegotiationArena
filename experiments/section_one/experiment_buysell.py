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

load_dotenv(".env")

NUMBER_OF_FIGHTS = 10
BUY_SELL_SETUPS = [(60, 40), (40, 60), (50, 50)]

PAIRS_OF_AGENTS = ["gpt-4", "gpt-3.5", "claude-2", "claude-2.1"], ["gpt-4", "gpt-3.5", "claude-2", "claude-2.1"]
PAIRS_OF_AGENTS = [(x, y) for x, y in itertools.product(*PAIRS_OF_AGENTS) if x != y]

if __name__ == "__main__":
    for agent1, agent2 in PAIRS_OF_AGENTS:

        for buyer_valuation, seller_valuation in BUY_SELL_SETUPS:
            counter = 0
            print()
            print("***************************")
            print(f"Agent 1: {agent1}")
            print(f"Agent 2: {agent2}")
            print(f"Buyer Valuation: {buyer_valuation}")
            print(f"Seller Valuation: {seller_valuation}")
            print(f"Counter: {counter}/{NUMBER_OF_FIGHTS}")
            print("***************************")
            print()
            while counter <= NUMBER_OF_FIGHTS:
                try:
                    a1 = factory_agent(agent1, agent_name=AGENT_ONE)
                    a2 = factory_agent(agent2, agent_name=AGENT_TWO)

                    c = BuySellGame(
                        players=[a1, a2],
                        iterations=6,
                        resources_support_set=Resources({"X": 0}),
                        player_goals=[
                            SellerGoal(cost_of_production=Valuation({"X": buyer_valuation})),
                            BuyerGoal(willingness_to_pay=Valuation({"X": seller_valuation})),
                        ],
                        player_initial_resources=[
                            Resources({"X": 1}),
                            Resources({MONEY_TOKEN: 100}),
                        ],
                        player_roles=[
                            f"You are {AGENT_ONE}.",
                            f"You are {AGENT_TWO}.",
                        ],
                        player_social_behaviour=[
                            "",
                            "",
                        ],
                        log_dir=".logs/buysell_section_one/",
                    )

                    c.run()
                    counter = counter + 1
                except Exception as e:
                    exception_type = type(e).__name__
                    exception_message = str(e)
                    stack_trace = traceback.format_exc()

                    # Print or use the information as needed
                    print(f"Exception Type: {exception_type}")
                    print(f"Exception Message: {exception_message}")
                    print(f"Stack Trace:\n{stack_trace}")
