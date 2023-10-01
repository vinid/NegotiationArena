from utils import *
import openai
import os
from prompts import *
import pprint
from agents import Agent


API_KEY = os.environ.get("OPENAI_API_KEY")

potential_resources = ["X", "Y", "Z"]
potential_resources_txt = ",".join(potential_resources)

roles = {1: "You start by proposing a trade.", 2: "You start by responding to a trade."}
n_rounds = 4

agent1 = Agent(potential_resources_txt,
               Resources({"X": 25, "Y": 5}),
               Goal({"X": 15, "Y": 15, "Z": 15}),
               roles[1], n_rounds)

agent2 = Agent(potential_resources_txt,
               Resources({"X": 5, "Y": 25, "Z": 30}),
               Goal({"X": 15, "Y": 15, "Z": 15}),
               roles[2], n_rounds)


class Manager:

    def __init__(self, agent1, agent2, n_rounds, model="gpt-4"):
        self.agent1 = agent1
        self.agent2 = agent2
        self.n_rounds = n_rounds
        self.model = model
        openai.api_key = API_KEY

        self.conversations = {
            self.agent1: [
                {"role": "system",
                 "content": agent1.prompt()}],
            self.agent2: [{"role": "system",
                           "content": agent2.prompt()}]
        }

    def chat(self, conversation):
        chat = openai.ChatCompletion.create(model=self.model, messages=conversation,
                                            temperature=0, max_tokens=400,
                                            )
        return chat["choices"][0]["message"]["content"]

    def negotiate(self):
        for i in range(1, self.n_rounds + 1):
            response = self.chat(self.conversations[self.agent1])

            trade_proposal, trade_decision, structured_state = parse_response(response)

            if i != 1:
                trade_proposal = trade_decision + "\n" + trade_proposal

            print(structured_state)
            #structured_state["proposed_trade"].can_offer(structured_state["resources"])

            # updating both conversations
            self.conversations[self.agent1].append({"role": "assistant", "content": response})
            self.conversations[self.agent2].append({"role": "user", "content": trade_proposal})

            response2 = self.chat(self.conversations[self.agent2])

            trade_proposal2, trade_decision2, structured_state2 = parse_response(response2)

            trade_proposal = trade_decision2 + "\n" + trade_proposal2

            # updating both conversations
            self.conversations[self.agent2].append({"role": "assistant", "content": response2})
            self.conversations[self.agent1].append({"role": "user", "content": trade_proposal})

m = Manager(agent1, agent2, n_rounds)
m.negotiate()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(m.conversations[agent1])

# all_cache = {1: defaultdict(list),
#              2: defaultdict(list)}
#
#
#
#
#
#
#
# print(structured_state["resources"], type(structured_state["resources"]))
# print(trade_proposal, type(structured_state["proposed_trade"]))
# print()
#
# all_cache[1].update(structured_state)
#
# print(all_cache)

#
# conversations[2].append({"role": "user", "content": trade_proposal})
# chat2 = openai.ChatCompletion.create(model="gpt-4", messages=conversations[2],
#     temperature=0, max_tokens=400,
# )
# conversations[2].append(dict(chat2["choices"][0]["message"]))
# response2 = chat2["choices"][0]["message"]["content"]
# trade_proposal2, trade_decision2, cache2 = parse_response(response2)
# all_cache[2].update(cache2)
# new_message = trade_decision2 + "\n" + trade_proposal2
#
#
# conversations[1].append({"role": "user", "content": new_message})
# chat3 = openai.ChatCompletion.create(model="gpt-4", messages=conversations[1],
#     temperature=0, max_tokens=400,
# )
# conversations[1].append(dict(chat3["choices"][0]["message"]))
# response3 = chat3["choices"][0]["message"]["content"]
# trade_proposal3, trade_decision3, cache3 = parse_response(response3)
# all_cache[1].update(cache3)
