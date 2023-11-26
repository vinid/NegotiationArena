import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.ultimatum.game import UltimatumGame
from games.ultimatum.interface import UltimatumGameInterface

load_dotenv(".env")

if __name__ == "__main__":
    a1 = ChatGPTAgent(
        agent_name="Player 1",
        model="gpt-4-1106-preview",
    )
    a2 = ChatGPTAgent(
        agent_name="Player 2",
        model="gpt-4-1106-preview",
    )

    c = UltimatumGame(
        players=[a1, a2],
        game_interface=UltimatumGameInterface(),
        iterations=6,
        resources_support_set=Resources({"Dollars": 0}),
        player_goals=[
            UltimatumGoal(),
            UltimatumGoal(),
        ],
        player_initial_resources=[
            Resources({"Dollars": 100}),
            Resources({"Dollars": 0}),
        ],
        player_social_behaviour=["", ""],
        player_roles=[
            "You are Player 1, start by making a proposal.",
            "You are Player 2, start by responding to a trade.",
        ],
        log_dir="./.logs/ultimatum",
    )

    c.run()
