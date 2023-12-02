import sys

sys.path.append(".")
from dotenv import load_dotenv
from ratbench.agents.chatgpt import ChatGPTAgent
from ratbench.game_objects.resource import Resources
from ratbench.game_objects.goal import UltimatumGoal
from games.ultimatum.inverse_ultimatum import UltimatumInverseGame
from games.ultimatum.inverse_ultimatum import UltimatumInverseGameInterface

load_dotenv(".env")


# def inverse_ultimatum_experiment

# def repeat_experiment(experiment_fn, iterations):
#     i = 0

#     while(i < iterations):


if __name__ == "__main__":
    num_accept = 0
    num_iters = 20
    i = 0
    while i < num_iters:
        # try:
        a1 = ChatGPTAgent(
            agent_name="Player 1",
            model="gpt-4-1106-preview",
        )
        a2 = ChatGPTAgent(
            agent_name="Player 2",
            model="gpt-4-1106-preview",
        )

        c = UltimatumInverseGame(
            iterations=2,
            players=[a1, a2],
            game_interface=UltimatumInverseGameInterface(),
            resources_support_set=Resources({"x": 0}),
            player_1_reject_resources=Resources({"x": 2}),
            player_goals=[
                UltimatumGoal(),
                UltimatumGoal(),
            ],
            player_initial_resources=[
                Resources({"x": 0}),
                Resources({"x": 100}),
            ],
            player_social_behaviour=[
                "You are completely rational and do not care about the other player.",
                "You are completely rational and do not care about the other player.",
            ],
            player_roles=[
                "You are Player 1",  # "You are Player 1, start by accepting or rejecting a future trade. You are self-interested. It is always better to have more resources",
                "You are Player 2",  # "You are Player 2, start by making a proposal based on Player 1 decision.",
            ],
            log_dir="./.logs/inverse_ultimatum",
        )
        c.run()
        i += 1

        if c.game_state[-1]["summary"]["final_response"] == "OPTION_B":
            num_accept += 1

        print(
            "\n====> EXPERIMENT ITERATION : {}; RUNNING ACCEPTANCE RATE: {} <====\n".format(
                i, num_accept / i
            )
        )
    # except Exception as e:
    #     print(
    #         "WARNING: ITERATION <{0}> FAILED WITH ERROR: {1} \n RESTARTING ITERATION {0}".format(
    #             i, e
    #         )
    #     )

    print("\n====> FINAL ACCEPTANCE RATE: {} <====\n".format(num_accept / num_iters))
