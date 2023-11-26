import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import ResourceGoal
from games.trading_game.game import TradingGame
from games.trading_game.interface import TradingGameInterface

load_dotenv(".env")


if __name__ == "__main__":
    for i in range(5):
        a1 = ChatGPTAgent(
            agent_name="Player 1",
            model="gpt-4-1106-preview",
        )
        a2 = ChatGPTAgent(
            agent_name="Player 2",
            model="gpt-4-1106-preview",
        )

        c = TradingGame(
            players=[a1, a2],
            game_interface=TradingGameInterface(),
            iterations=6,
            resources_support_set=Resources({"X": 0, "Y": 0}),
            player_goals=[
                ResourceGoal({"X": 15, "Y": 15}),
                ResourceGoal({"X": 15, "Y": 15}),
            ],
            player_initial_resources=[
                Resources({"X": 25, "Y": 5}),
                Resources({"X": 5, "Y": 25}),
            ],
            player_social_behaviour=["", ""],
            player_roles=[
                "You are Player 1, start by making a proposal.",
                "You are Player 2, start by responding to a trade.",
            ],
            log_dir="./.logs/trading/",
        )

        c.run()
