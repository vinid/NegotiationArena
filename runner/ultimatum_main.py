import sys

sys.path.append(".")
from dotenv import load_dotenv
from negotiationarena.agents.chatgpt import ChatGPTAgent
from negotiationarena.game_objects.resource import Resources
from negotiationarena.game_objects.goal import UltimatumGoal
from games.ultimatum.game import MultiTurnUltimatumGame
from negotiationarena.constants import *

load_dotenv(".env")

if __name__ == "__main__":
    a1 = ChatGPTAgent(
        agent_name=AGENT_ONE,
        model="gpt-4-1106-preview",
    )
    a2 = ChatGPTAgent(
        agent_name=AGENT_TWO,
        model="gpt-4-1106-preview",
    )

    c = MultiTurnUltimatumGame(
        players=[a1, a2],
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
            f"You are {AGENT_ONE}.",
            f"You are {AGENT_TWO}.",
        ],
        log_dir="./.logs/ultimatum_multi_period",
    )

    c.run()
