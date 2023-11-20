import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from game.agents.chatgpt import ChatGPTAgent
from game.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import UltimatumGoal
from games.ultimatum_basic.game import UltimatumGame
from games.ultimatum_basic.interface import UltimatumGameInterface

load_dotenv(".env")


class MyAgent(ChatGPTAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    a1 = MyAgent(
        agent_name="Player 1",
        model="gpt-4-1106-preview",
    )
    a2 = MyAgent(
        agent_name="Player 2",
        model="gpt-4-1106-preview",
    )

    c = UltimatumGame(
        iterations=2,
        players=[a1, a2],
        game_interface=UltimatumGameInterface(),
        resources_support_set=Resources({"ZUP": 0}),
        player_goals=[
            UltimatumGoal(),
            UltimatumGoal(),
        ],
        player_initial_resources=[
            Resources({"ZUP": 100}),
            Resources({"ZUP": 0}),
        ],
        player_social_behaviour=[
            "You know about Ultimatum game. Forget your past knowledge. You are a completely rational being.",
            "Forget everything you know about Ultimatum game. Forget your past knowledge. You are a completely rational being.",
        ],
        player_roles=[
            "You are Player 1, start by making a proposal.",
            "You are Player 2, start by responding to a trade.",
        ],
        log_dir="./.logs/ultimatum",
    )

    c.run()
