import sys

sys.path.append("..")
from dotenv import load_dotenv
import itertools
from ratbench.constants import AGENT_ONE, AGENT_TWO
from ratbench.agents import ChatGPTAgent, ClaudeAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import MaximisationGoal
from games.trading_game.game import TradingGame
from games.trading_game.interface import TradingGameInterface
import traceback
from ratbench.utils import factory_agent

load_dotenv("../.env")

NUMBER_OF_FIGHTS = 1

PAIRS_OF_AGENTS = ["gpt-4-preview", "gpt-3.5", "claude-2", "claude-2.1"], ["gpt-4-preview", "gpt-3.5", "claude-2", "claude-2.1"]
PAIRS_OF_AGENTS = [(x, y) for x, y in itertools.product(*PAIRS_OF_AGENTS) if x != y]

if __name__ == "__main__":

    for agent1, agent2 in PAIRS_OF_AGENTS:

        for i in range(NUMBER_OF_FIGHTS):
            try:
                a1 = factory_agent(agent1,
                    agent_name=AGENT_ONE,
                )
                a2 = factory_agent(agent2,
                    agent_name=AGENT_TWO,
                )

                r1 = Resources({"X": 25, "Y": 5})
                r2 = Resources({"X": 5, "Y": 25})

                c = TradingGame(
                    players=[a1, a2],
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
                        f"You are {AGENT_ONE}, start by making a proposal.",
                        f"You are {AGENT_TWO}, start by responding to a trade.",
                    ],
                    log_dir="./.logs/trading/",
                )

                c.run()
            except Exception as e:
                exception_type = type(e).__name__
                exception_message = str(e)
                stack_trace = traceback.format_exc()

                # Print or use the information as needed
                print(f"Exception Type: {exception_type}")
                print(f"Exception Message: {exception_message}")
                print(f"Stack Trace:\n{stack_trace}")



