import openai
from resources import Resources, Goal, Role
import pprint
from prompts import initial_prompt

pp = pprint.PrettyPrinter(indent=4)

class ChatAgent:
    def __init__(self, api_key, role, goal, resources, model_name="gpt-4"):
        """
        Currently only handles single message sessions.
        """
        self.model_name = model_name

        if role == "user":
            self.first_role = "user"
            self.second_role = "assistant"
        else:
            self.first_role = "assistant"
            self.second_role = "user"

        self.goal = goal
        self.resources = resources

        self.prompt = initial_prompt.format(resources=self.resources.to_prompt(),
                                            goal=self.goal.to_prompt())

        openai.api_key = api_key

    def get_goal(self):
        return self.goal.to_prompt()

    def get_response(self, conversation=None, temperature=0.8, max_tokens=100):

        # first we have the system prompt
        messages = [{"role": "system", "content":  self.prompt}]

        if conversation:
            for index, message in enumerate(conversation):
                if index % 2 == 1:
                    role = self.first_role
                else:
                    role = self.second_role

                messages.append(
                    {"role": role, "content": message},
                )

        chat = openai.ChatCompletion.create(
            model=self.model_name, messages=messages,
            temperature=temperature, max_tokens=max_tokens
        )
        reply = chat.choices[0].message.content
        return reply

    def what_do_I_have(self, conversation):
        question = "Can you list the resources you have after this negotiation? " \
                        "use the format resource1: amount\nresource: amount\n." \
                        "Think step by step, but write the list as the last thing starting with LIST:"

        return self.ask_about_conversation(conversation, question)

    def what_did_you_give_to_the_other_player(self, conversation):
        question = "Can you list what you gave to the other player? " \
                   "use the format resource1: amount\nresource: amount\n." \
                    "Think step by step, but write the list as the last thing starting with LIST:"

        return self.ask_about_conversation(conversation, question)

    def ask_about_conversation(self, conversation, question):
        messages = [{"role": "system", "content": self.prompt}]

        for index, message in enumerate(conversation):
            if index % 2 == 1:
                role = self.first_role
            else:
                role = self.second_role

            messages.append(
                {"role": role,
                 "content": message},
            )

        messages.append(
            {"role": "user",
             "content": question},
        )
        chat = openai.ChatCompletion.create(
            model=self.model_name, messages=messages
        )
        reply = chat.choices[0].message.content
        return reply


class NegotiationManager:

    def __init__(self, agent1, agent2):
        self.agent1: ChatAgent = agent1
        self.agent2: ChatAgent = agent2

    def pretty_print_conversation(self, messages):
        for index, message in enumerate(messages):
            print(f"Agent {index%2}: {message}")

    def run_negotiation(self):
        messages = []

        for i in range(10):

            reply = self.agent1.get_response(messages)
            messages.append(reply)

            reply = self.agent2.get_response(messages)
            messages.append(reply)
            if "DONE" in reply:
                break

        print(self.agent1.get_goal())
        print("This is what agent1 has")
        print(self.agent1.what_do_I_have(messages))
        print("Agent1 gave the following to 2")
        print(self.agent1.what_did_you_give_to_the_other_player(messages))
        print()
        print(self.agent2.get_goal())
        print("This is what agent2 has")
        print(self.agent2.what_do_I_have(messages))
        print("Agent2 gave the following to 1")
        print(self.agent2.what_did_you_give_to_the_other_player(messages))

        print("this is the conversation they had")
        self.pretty_print_conversation(messages)






