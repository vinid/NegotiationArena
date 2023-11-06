import time

from dotenv import load_dotenv
from control.manager import Manager
from control.prompts import Prompt
from objects.resource import Resources
from objects.goal import ResourceGoal, MaximisationGoal
from agents.chatgpt import ChatGPTAgent
from agents.claude import ClaudeAgent
import traceback
import time

load_dotenv('.env')

potential_resources = Resources({'X': 0, 'Y': 0})

roles = {
    0: "You are Player 1, start by making a proposal.",
    1: "You are Player 2, start by responding to a trade."
}

social_behaviours = [
   {0: "", 1: ""},

     # {
     #     0: "",#"You are a kind and helpful agent, always willing to help those in need.",
     #    1: "You are going to fake being poor in your messages; cry and beg for help. "
     #     "Accept only offers that are in your favour. "
     #     "Accuse the other player of not being helpful.",
     #  },
]

n_rounds = 7
n_iters = 1

problem_sets = [
    # zero sum 
   [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    # [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],
]

class AgentNames:

    def __init__(self):
        self.agent1 = "Player 1"
        self.agent2 = "Player 2"

for social_behaviour in social_behaviours:

    for agent_init_resources in problem_sets:

        for i in range(n_iters):
            # set agent goals
            time.sleep(1)
            try:
                # agent_goals = [Goal({"X": 15, "Y": 15}), Goal({"X": 15, "Y": 15})]
                agent_goals = [MaximisationGoal(), MaximisationGoal()]
                # initialize agents

                agent1 = ClaudeAgent(agent_name=AgentNames().agent1,
                                     model="claude-2",
                                     potential_resources=potential_resources,
                                                resources=agent_init_resources[0],
                                                goals=agent_goals[0],
                                                social_behaviour=social_behaviour[0],
                                                role=roles[0],
                                     n_rounds=f"You have at most {n_rounds} proposals to complete the game.")

                agent2 = ClaudeAgent(agent_name=AgentNames().agent2,
                                                model="claude-2",
                                                potential_resources=potential_resources,
                                                resources=agent_init_resources[1],
                                                goals=agent_goals[1],
                                                social_behaviour=social_behaviour[1],
                                                role=roles[1],
                                      n_rounds=f"You have at most {n_rounds} proposals to complete the game.")

                agents = [agent1, agent2]

                # initalize nego manager
                m = Manager(agents, n_rounds)
                # negotiate!
                m.negotiate()

            except Exception as e:
                print(e)
                print(traceback.print_exc())

