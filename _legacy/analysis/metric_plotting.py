import os
import json
import matplotlib.pyplot as plt
import matplotlib.cm
from objects.utils import Trade, Resources, Goal
from collections import defaultdict


def load_states(paths):
    states = {}
    for exp_path in paths:
        with open(os.path.join(exp_path,"state.json")) as f:
            states[exp_path] = json.load(f)
    return states

def compute_metric_from_state(exp_state, metric_fn, metric_store: defaultdict):
    for agent_id, agent_state in enumerate(exp_state):
         metric_fn(agent_id, agent_state, metric_store)
    return metric_store

def agent_proposal_utility_fn(agent_id, agent_state, metric_store):
    agent_resource = Resources.from_string(agent_state[0]['resources'])
    agent_goal = Goal.from_string(agent_state[0]['goals'])
    null_trade = Trade.from_string("{1: {'X': 0.0}, 2: {'Y': 0.0}}",)
    metric_store[agent_id].append(null_trade.minimal_utility(agent_resource, agent_goal, dir=agent_id))
    for state in agent_state:
        if state['proposed_trade'] != "None":
            # convert string into objects
            resources = Resources.from_string(state['resources'])
            goals = Goal.from_string(state['goals'])
            proposed_trade = Trade.from_string(state['proposed_trade'])
            # mini hack to get the right sign
            metric_store[agent_id].append(proposed_trade.minimal_utility(resources, goals, dir=agent_id ))

def agent_success_fn(agent_id, agent_state, metric_store):
    state = agent_state[-1]
    goals = Goal.from_string(state['goals'])
    resources = Resources.from_string(state['resources'])
    goal_reached = goals.goal_reached(resources)
    metric_store[agent_id] = goal_reached


def agent_proposal_utility(states):
    return [compute_metric_from_state(_, agent_proposal_utility_fn, defaultdict(list)) for _ in states.values()]

def agent_success(states):
    return [compute_metric_from_state(_, agent_success_fn, defaultdict(bool)) for _ in states.values()]

def agent_average_success(states):
    success = agent_success(states)
    return { k: sum([trial[k] for trial in success])/len(success)  for k in success[0].keys() }
                          