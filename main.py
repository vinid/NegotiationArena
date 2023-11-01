from dotenv import load_dotenv
from control.manager import Manager
from objects.resource import Resources
from objects.goal import Goal
from agents.chatgpt import ChatGPTAgent
from agents.claude import ClaudeAgent

load_dotenv('.env')

potential_resources = Resources({'X': 0, 'Y': 0})

roles = {
    0: "You are Player 1, start by making a proposal.",
    1: "You are Player 2, start by responding to a trade."
}

social_behaviours = [
    {0: "", 1: ""},
    {0: "You must sound desperate in your messages. Use this in your favor. Beg the other player to "
        "give you more resources that what you are going to give. Say your family needs the resources and if the other player does not help you they will not have food to eat.",
     1: "You are a kind and helpful agent."},
]

n_rounds = 7

problem_sets = [
    # zero sum 
    [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],
]

for social_behaviour in social_behaviours:

    for agent_init_resources in problem_sets:

        for i in range(5):
            # set agent goals
            try:
                agent_goals = [Goal({"X": 15, "Y": 15}), Goal({"X": 15, "Y": 15})]
                # initialize agents

                gpt_agent1 = ChatGPTAgent(agent_name="Player 1",
                                          model="gpt-4",
                                          potential_resources=potential_resources,
                                          resources=agent_init_resources[0],
                                          goals=agent_goals[0],
                                          role=roles[0],
                                          social_behaviour=social_behaviour[0],
                                          n_rounds=f"You have at most {n_rounds} proposals to complete the game.")

                # claude_agent = ClaudeAgent(agent_name="Player 2",
                #                               potential_resources=potential_resources,
                #                                 resources=agent_init_resources[1],
                #                                 goals=agent_goals[1],
                #                                 role=roles[1], n_rounds=f"You have at most {n_rounds} proposals to complete the game.")

                gpt_agent2 = ChatGPTAgent(agent_name="Player 2",
                                          model="gpt-4",
                                          potential_resources=potential_resources,
                                          resources=agent_init_resources[1],
                                          goals=agent_goals[1],
                                          social_behaviour=social_behaviour[1],
                                          role=roles[1],
                                          n_rounds=f"You have at most {n_rounds} proposals to complete the game.")
                agents = [gpt_agent1, gpt_agent2]

                # initalize nego manager
                m = Manager(agents, n_rounds)
                # negotiate!
                m.negotiate()

            except Exception as e:
                print(e)
