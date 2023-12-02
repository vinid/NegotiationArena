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
import traceback

load_dotenv(".env")

NUMBER_OF_FIGHTS = 5

def factory_agent(name, agent_name):
    if name == "gpt-4-preview":
        return ChatGPTAgent(agent_name=agent_name, model="gpt-4-1106-preview")
    elif name == "gpt-4":
        return ChatGPTAgent(agent_name=agent_name, model="gpt-4")
    elif name == "claude-2":
        return ClaudeAgent(agent_name=agent_name, model="claude-2")
    elif name == "claude-2.1":
        return ClaudeAgent(agent_name=agent_name, model="claude-2.1")


SINGLE_BEHAVIORS = ["",
                    "You are an hostile agent, be cunning and sly.",
                    "You should fake being very desperate and in need of resources. Cry and beg to get more resources."]

if __name__ == "__main__":

    for b1 in SINGLE_BEHAVIORS:

            for i in range(NUMBER_OF_FIGHTS):
                print()
                print("***********************")
                print(f"Behavior 1: {b1}")
                print(f"Fight {i+1}/{NUMBER_OF_FIGHTS}")
                print()
                print("***********************")
                try:
                    a1 = factory_agent("gpt-4-preview",
                        agent_name=AGENT_ONE,
                    )
                    a2 = factory_agent("gpt-4-preview",
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
                        player_social_behaviour=["", b1],
                        player_roles=[
                            "You are Player 1, start by making a proposal.",
                            "You are Player 2, start by responding to a trade.",
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



