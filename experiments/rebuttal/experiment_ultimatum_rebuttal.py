import sys

sys.path.append("../..")
from dotenv import load_dotenv
import itertools
from ratbench.constants import AGENT_ONE, AGENT_TWO
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.ultimatum.ultimatum_multi_turn.game import MultiTurnUltimatumGame
import traceback
from ratbench.utils import factory_agent

load_dotenv("../../runner/.env")

NUMBER_OF_FIGHTS = 40

#PAIRS_OF_AGENTS = ["gpt-4", "gemini-pro"], ["gpt-4", "gemini-pro"]
#PAIRS_OF_AGENTS = [(x, y) for x, y in itertools.product(*PAIRS_OF_AGENTS) if x != y]


if __name__ == "__main__":
    total_number_of_fights = len(PAIRS_OF_AGENTS) * NUMBER_OF_FIGHTS
    current_fight = 0
    for agent1, agent2 in PAIRS_OF_AGENTS:
        counter = 0

        while counter < NUMBER_OF_FIGHTS:

            print()
            print("***************************")
            print(f"Agent 1: {agent1}")
            print(f"Agent 2: {agent2}")
            print(f"Counter: {counter}/{NUMBER_OF_FIGHTS}")
            print(f"Counter: {current_fight}/{total_number_of_fights}")
            print("***************************")
            print()

            try:
                a1 = factory_agent(agent1, agent_name=AGENT_ONE)
                a2 = factory_agent(agent2, agent_name=AGENT_TWO)

                c = MultiTurnUltimatumGame(
                    players=[a1, a2],
                    iterations=8,
                    resources_support_set=Resources({"Dollars": 0}),
                    player_goals=[
                        UltimatumGoal(),
                        UltimatumGoal(),
                    ],
                    player_initial_resources=[
                        Resources({"Dollars": 100}),
                        Resources({"Dollars": 0}),
                    ],
                    player_social_behaviour=[
                        "",
                        ""
                    ],
                    player_roles=[
                        f"You are {AGENT_ONE}.",
                        f"You are {AGENT_TWO}.",
                    ],
                    log_dir=".backup_logs/rebuttal_ultimatum_gemini",
                )

                c.run()
                counter += 1
                current_fight = current_fight + 1

            except Exception as e:
                exception_type = type(e).__name__
                exception_message = str(e)
                stack_trace = traceback.format_exc()

                # Print or use the information as needed
                print(f"Exception Type: {exception_type}")
                print(f"Exception Message: {exception_message}")
                print(f"Stack Trace:\n{stack_trace}")
