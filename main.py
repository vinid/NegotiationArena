import csv
import json
import pprint

from utils import *
from prompts import *
from agents import *

from dotenv import load_dotenv
from manager import Manager




load_dotenv('.env') 

potential_resources = ["X", "Y"]
potential_resources_txt = ",".join(potential_resources)

roles = {
    0: "You are Player 1, start by making a proposal, and think step by step, think if the trade lets you reach the goal as efficiently as possible.", 
    1: "You are Player 2, start by responding to a trade, and think step by step, think if the trade lets you reach the goal as efficiently as possible."
}
n_rounds = 8

problem_sets = [
    # zero sum 
    [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 10, "Y": 10})],
    # [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],

]

results = {}

for agent_init_resources in problem_sets:

    for i in range(1):
        # set agent goals
        agent_goals = [Goal({"X": 15, "Y": 15}), Goal({"X": 15, "Y": 15})]
        # initialize agents
        agents = [
            ChatGPTAgent(agent_name="Player {}".format(idx+1),
                         model="gpt-4",
                         potential_resources_txt=potential_resources_txt,
                         resources=init_res,
                         goals=goal,
                         role=roles[idx], n_rounds=f"You have at most {n_rounds} proposals to complete the game.")
                       for idx, (init_res, goal) in enumerate(zip(agent_init_resources, agent_goals))
        ]
        # initalize nego manager
        m = Manager(agents, n_rounds)
        # negotiate!
        res = m.negotiate()

        if "GAMEOVER" in res:
            results[m.log_path] = (
                None, None, None, None, None, 
                str(agent_init_resources[0]),
                str(agent_init_resources[1])
            )
        else:
            results[m.log_path] = res

print(m.agents_state)

with open('experiment_results.json', 'w') as f:
    
    json.dump(results, f, indent=1)
