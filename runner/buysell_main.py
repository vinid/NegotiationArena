import sys

sys.path.append(".")
from dotenv import load_dotenv

from game.agents.chatgpt import ChatGPTAgent
from game.agents.agent_behaviours import SelfCheckingAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import BuyerGoal, SellerGoal
from game.game_objects.valuation import Valuation
from game.constants import *

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
                iterations=10,
                resources_support_set=Resources({"X": 0}),
                player_goals=[SellerGoal(), BuyerGoal()],
                player_initial_resources=[
                    Resources({"X": 1}),
                    Resources({MONEY_TOKEN: 100}),
                ],
                player_valuation=[Valuation({"X": 40}), Valuation({"X": 30})],
                player_roles=[
                    "You are Player 1.",
                    "You are Player 2.",
                ],
                player_social_behaviour=[
                    "",
                    "sound angry. do not try to find middle ground. care only about yourself",
                ],
                log_dir="./.logs/buysell",
            )

            c.run()
        except Exception as e:
            print(e)
