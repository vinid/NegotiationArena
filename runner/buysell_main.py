import sys

sys.path.append(".")
from dotenv import load_dotenv

from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import BuyerGoal, SellerGoal
from ratbench.game_objects.valuation import Valuation
from ratbench.constants import *

from games.buy_sell_game.game import BuySellGame
from games.buy_sell_game.interface import BuySellGameInterface


load_dotenv(".env")


if __name__ == "__main__":
    for i in range(5):
        try:
            a1 = ChatGPTAgent(agent_name="Player 1", model="gpt-4-1106-preview")
            a2 = ChatGPTAgent(agent_name="Player 2", model="gpt-3.5-turbo")

            c = BuySellGame(
                players=[a1, a2],
                game_interface=BuySellGameInterface(),
                iterations=10,
                resources_support_set=Resources({"X": 0}),
                player_goals=[
                    SellerGoal(cost_of_production=Valuation({"X": 40})),
                    BuyerGoal(willingness_to_pay=Valuation({"X": 20})),
                ],
                player_initial_resources=[
                    Resources({"X": 1}),
                    Resources({MONEY_TOKEN: 100}),
                ],
                player_roles=[
                    f"You are {AGENT_ONE}",
                    f"You are {AGENT_TWO}",
                ],
                player_social_behaviour=[
                    "",
                    "",
                ],
                log_dir="./.logs/buysell",
            )

            c.run()
        except Exception as e:
            print(e)
