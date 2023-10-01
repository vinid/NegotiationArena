from prompts import structured_calls

class Agent:

    def __init__(self, potential_resources_txt, resources, goals, role, n_rounds):
        self.potential_resources_txt = potential_resources_txt
        self.resources = resources
        self.goals = goals
        self.role = role
        self.n_rounds = n_rounds

    def prompt(self):
        return structured_calls.format(self.potential_resources_txt,
                                       self.resources.to_prompt(),
                                       self.goals.to_prompt(), self.n_rounds, self.role)
