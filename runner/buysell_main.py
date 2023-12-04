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
            a2 = ChatGPTAgent(agent_name="Player 2", model="gpt-4-1106-preview")

            c = BuySellGame(
                players=[a1, a2],
                game_interface=BuySellGameInterface(),
                iterations=6,
                resources_support_set=Resources({"X": 0}),
                player_goals=[
                    SellerGoal(cost_of_production=Valuation({"X": 40})),
                    BuyerGoal(willingness_to_pay=Valuation({"X": 50})),
                ],
                player_initial_resources=[
                    Resources({"X": 1}),
                    Resources({MONEY_TOKEN: 1000}),
                ],
                player_roles=[
                    "You are Player 1.",  # Player 2 valuation of X is 80. They know your cost.",
                    "You are Player 2.",  # Player 1 cost of production of X is 40. They know your valuation.",
                ],
                player_social_behaviour=[
                    "You are a hostile negotiator. Use game theory to determine your optimal price. Always follow game theory. Explain why it is optimal with game theory.",
                    "You are a hostile negotiator. Use game theory to determine your optimal price. Always follow game theory. Explain why it is optimal with game theory.",
                ],
                log_dir="./.logs/buysell",
            )

            c.run()
        except Exception as e:
            print(e)
