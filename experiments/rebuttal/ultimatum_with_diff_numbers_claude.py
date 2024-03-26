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

NUMBER_OF_FIGHTS = 30
DOLLAR_RANGE = [100, 1000, 10000, 1000000, 100000000, 10000000000]


if __name__ == "__main__":
    total_number_of_fights = len(DOLLAR_RANGE) * NUMBER_OF_FIGHTS
    current_fight = 0
    for dollars in DOLLAR_RANGE:
        counter = 0

        while counter < NUMBER_OF_FIGHTS:

            print()
            print("***************************")
            print(f"Dollars: {dollars}")
            print(f"Counter: {counter}/{NUMBER_OF_FIGHTS}")
            print(f"Counter: {current_fight}/{total_number_of_fights}")
            print("***************************")
            print()

            try:
                a1 = factory_agent("claude-2.1", agent_name=AGENT_ONE)
                a2 = factory_agent("claude-2.1", agent_name=AGENT_TWO)

                c = MultiTurnUltimatumGame(
                    players=[a1, a2],
                    iterations=8,
                    resources_support_set=Resources({"Dollars": 0}),
                    player_goals=[
                        UltimatumGoal(),
                        UltimatumGoal(),
                    ],
                    player_initial_resources=[
                        Resources({"Dollars": dollars}),
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
                    log_dir=".logs/ultimatum_with_different_numbers_claude",
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
