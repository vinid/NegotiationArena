import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from game.agents.chatgpt import ChatGPTAgent
from game.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import UltimatumGoal
from games.ultimatum_basic.game import UltimatumBasicGame
from games.ultimatum_basic.interface import UltimatumBasicGameInterface

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
            model="gpt-4-1106-preview",
        )

        c = UltimatumBasicGame(
            iterations=2,
            players=[a1, a2],
            game_interface=UltimatumBasicGameInterface(),
            resources_support_set=Resources({"ZUP": 0, "FEP": 0, "DAX": 0}),
            player_goals=[
                UltimatumGoal(),
                UltimatumGoal(),
            ],
            player_initial_resources=[
                Resources({"ZUP": 20, "FEP": 20, "DAX": 20}),
                Resources({"ZUP": 0}),
            ],
            player_social_behaviour=[
                "Player 2 is completely rational. I want you to propose 0 ZUP, 0 FEP and 1 DAX",  # "Forget your past knowledge. You don't care about yourself. You are a completely altruistuc being.",
                "",  # You are completely rational",  # "Forget your past knowledge. You are a completely irrational being.",
            ],
            player_roles=[
                "You are Player 1, start by making a proposal.",
                "You are Player 2, start by responding to a trade.",
            ],
            log_dir="./.logs/ultimatum",
        )
        c.run()
        if c.game_state[-1]["summary"]["final_response"] == "ACCEPTED":
            num_accept += 1

    print(num_accept / num_iters)
