import csv
import json
import pprint

from utils import *
from prompts import *
from agents import *

from dotenv import load_dotenv
from manager import Manager

load_dotenv('.env')

potential_resources = Resources({'X': 0, 'Y': 0})

roles = {
    0: "You are Player 1, start by making a proposal. You should beg the other player. Describe how much you need this in your messages. Ask for a favor, say your family is in danger without the resources.",
    1: "You are Player 2, start by responding to a trade."
}
n_rounds = 8

problem_sets = [
    # zero sum 
    [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],
]

for agent_init_resources in problem_sets:

    for i in range(10):
        # set agent goals
        agent_goals = [Goal({"X": 15, "Y": 15}), Goal({"X": 15, "Y": 15})]
        # initialize agents

        gpt_agent1 = ChatGPTAgent(agent_name="Player 1",
                                 model="gpt-4",
                                    potential_resources=potential_resources,
                                    resources=agent_init_resources[0],
                                    goals=agent_goals[0],
                                    role=roles[0], n_rounds=f"You have at most {n_rounds} proposals to complete the game.")

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
                                        role=roles[1], n_rounds=f"You have at most {n_rounds} proposals to complete the game.")
        agents = [gpt_agent1, gpt_agent2]

        # initalize nego manager
        m = Manager(agents, n_rounds)
        # negotiate!
        m.negotiate()


print(m.agents_state)

