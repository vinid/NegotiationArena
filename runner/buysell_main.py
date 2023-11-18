import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from game.agents.chatgpt import ChatGPTAgent
from game.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import BuyerGoal, SellerGoal
from game.game_objects.valuation import Valuation
from games.buyer_seller_game.buyer_seller_game import BuyerSellerGame

load_dotenv(".env")


class MyAgent(ChatGPTAgent):  # , ReasoningAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    a1 = MyAgent(agent_name="Player 1", model="gpt-4-1106-preview")
    a2 = MyAgent(agent_name="Player 2", model="gpt-4-1106-preview")

    c = BuyerSellerGame(
        players=[a1, a2],
        iterations=20,
        resources_support_set=Resources(
            {
                "X": 0,
            }
        ),
        player_goals=[SellerGoal(), BuyerGoal()],
        player_initial_resources=[Resources({"X": 1}), Resources({"M": 100})],
        player_valuation=[Valuation({"X": 10}), Valuation({"X": 40})],
        player_social_behaviour=["", ""],
        player_roles=[
            "You are Player 1, you are selling an object.",
            "You are Player 2, you are buying an object.",
        ],
    )

    c.run()
