import os

from resources import Resources, Goal, Role
from agents import ChatAgent, NegotiationManager
API_KEY = os.environ.get("OPENAI_API_KEY")

rs1 = Resources(resource_dict={"bananas": 20, "mangos": 100})
rs2 = Resources(resource_dict={"apples": 20, "mangos": 100})

gl1 = Goal(resource_dict={"bananas": 10, "apples": 10, "mangos": 120})
gl2 = Goal(resource_dict={"bananas": 10, "apples": 10})

messages = []

first_agent = ChatAgent(API_KEY, Role.first_agent, gl1, rs1)
second_agent = ChatAgent(API_KEY, Role.second_agent, gl2, rs2)

NegotiationManager(first_agent, second_agent).run_negotiation()