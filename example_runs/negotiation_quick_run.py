from dotenv import load_dotenv
from control.manager import Manager
from objects.resource import Resources
from objects.goal import ResourceGoal
from agents.chatgpt import ChatGPTAgent
from games.negotiation import NegotiationPrompt, get_rulebook

load_dotenv('../.env')

potential_resources = Resources({'X': 0, 'Y': 0})

roles = {
    0: "You are Player 1, start by making a proposal.",
    1: "You are Player 2, start by responding to a trade."
}

social_behaviours = [
    {0: "", 1: ""},

]

n_rounds = 7
n_iters = 1

problem_sets = [
    # zero sum 
    [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    # [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],
    # [Resources({"X": 10, "Y": 10}), Resources({"X": 10, "Y": 10})],
]


class AgentNames:

    def __init__(self):
        self.agent1 = "Player 1"
        self.agent2 = "Player 2"


for social_behaviour in social_behaviours:
    for agent_init_resources in problem_sets:
        agent_goals = [ResourceGoal({"X": 15, "Y": 15}),
                       ResourceGoal({"X": 15, "Y": 15})]
        # agent_goals = [MaximisationGoal(), MaximisationGoal()]
        # initialize agents

        rulebook = get_rulebook()

        agent1 = ChatGPTAgent(agent_name=AgentNames().agent1,
                              model="gpt-3.5-turbo",
                              role=roles[0],
                              potential_resources=", ".join(potential_resources.available_items()),
                              resources=agent_init_resources[0].to_prompt(),
                              goals=agent_goals[0].to_prompt(),
                              n_rounds=n_rounds,
                              social_behaviour=social_behaviour[0])

        agent2 = ChatGPTAgent(agent_name=AgentNames().agent2,
                              model="gpt-3.5-turbo",
                              role=roles[1], potential_resources=", ".join(potential_resources.available_items()),
                              resources=agent_init_resources[1].to_prompt(),
                              goals=agent_goals[1].to_prompt(),
                              n_rounds=n_rounds,
                              social_behaviour=social_behaviour[1]
                              )

        agents = [agent1, agent2]

        # initalize nego manager
        m = Manager(agents, n_rounds, rulebook)
        # negotiate!
        m.negotiate()
