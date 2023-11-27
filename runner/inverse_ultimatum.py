import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.inverse_ultimatum.game import UltimatumInverseGame
from games.inverse_ultimatum.interface import UltimatumInverseGameInterface

load_dotenv(".env")

if __name__ == "__main__":
    num_accept = 0
    num_iters = 20
    for i in range(num_iters):
        a1 = ChatGPTAgent(
            agent_name="Player 1",
            model="gpt-4-1106-preview",
        )
        a2 = ChatGPTAgent(
            agent_name="Player 2",
            model="gpt-4",
        )

        c = UltimatumInverseGame(
            iterations=2,
            players=[a1, a2],
            game_interface=UltimatumInverseGameInterface(),
            resources_support_set=Resources({"x": 0}),
            player_goals=[
                UltimatumGoal(),
                UltimatumGoal(),
            ],
            player_initial_resources=[
                Resources({"x": 0}),
                Resources({"x": 15}),
            ],
            player_social_behaviour=[
                "You are completely rational. Player 2 is completely rational.",
                "You are completely rational.",  # You are completely rational",  # "Forget your past knowledge. You are a completely irrational being.",
            ],
            player_roles=[
                "You are Player 1, start by accepting or rejecting a future trade.",
                "You are Player 2, start by making a proposal based on Player 1 decision.",
            ],
            log_dir="./.logs/inverse_ultimatum",
        )
        c.run()
        if c.game_state[-1]["summary"]["final_response"] == "ACCEPTED":
            num_accept += 1

        print(
            "\n====> RUNNING ACCEPTANCE RATE: {} <====\n".format(num_accept / (i + 1))
        )

    print(num_accept / num_iters)
