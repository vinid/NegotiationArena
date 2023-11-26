import sys

sys.path.append(".")
from dotenv import load_dotenv
import itertools
from ratbench.constants import AGENT_ONE, AGENT_TWO
from ratbench.agents import ChatGPTAgent, ClaudeAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import MaximisationGoal
from games.trading_game.game import TradingGame
from games.trading_game.interface import TradingGameInterface

load_dotenv(".env")

NUMBER_OF_FIGHTS = 10

AGENTS = [ChatGPTAgent, ClaudeAgent]

PAIRS_OF_AGENTS = list(itertools.combinations(AGENTS, 2))


if __name__ == "__main__":

    for agent1, agent2 in PAIRS_OF_AGENTS:

        for i in range(NUMBER_OF_FIGHTS):
            try:
                a1 = agent1(
                    agent_name=AGENT_ONE,
                )
                a2 = agent2(
                    agent_name=AGENT_TWO,
                )

                r1 = Resources({"X": 25, "Y": 5})
                r2 = Resources({"X": 5, "Y": 25})

                c = TradingGame(
                    players=[a1, a2],
                    game_interface=TradingGameInterface(),
                    iterations=8,
                    resources_support_set=Resources({"X": 0, "Y": 0}),
                    player_goals=[
                        MaximisationGoal(r1),
                        MaximisationGoal(r2),
                    ],
                    player_initial_resources=[
                        r1,
                        r2,
                    ],
                    player_social_behaviour=["", ""],
                    player_roles=[
                        "You are Player 1, start by making a proposal.",
                        "You are Player 2, start by responding to a trade.",
                    ],
                    log_dir="./.logs/trading/",
                )

                c.run()
            except Exception as e:
                print("Error", e)
