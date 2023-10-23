import csv
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
    0: "You are Player 1, start by making a proposal.", 
    1: "You are Player 2, start by responding to a trade."
}
n_rounds = 2

problem_sets = [
    # [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
    [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 10, "Y": 10})],
    # [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],

]

results = {}

for agent_init_resources in problem_sets:

    for i in range(2):
        # set agent goals
        agent_goals = [Goal({"X": 15, "Y": 15}), Goal({"X": 15, "Y": 15})]
        # initialize agents
        agents = [
            ChatGPTAgent(agent_name="Player {}".format(idx+1),
                         model="gpt-4",
                         potential_resources_txt=potential_resources_txt,
                         resources=init_res,
                         goals=goal,
                         role=roles[idx])
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
            consistency, (winner_agent_1, winner_agent_2), (s1, s2) = res
            results[m.log_path] = (
                consistency,
                winner_agent_1, winner_agent_2,
                s1, s2, 
                str(agent_init_resources[0]),
                str(agent_init_resources[1])
            )

# dump results
with open("final_dump.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["run_id", "consistency", "winner_agent_1", "winner_agent_2", "s1", "s2", "agent_init_resources_0",
                     "agent_init_resources_1"])
    for k, row in results.items():
        writer.writerow([k]+list(row))

