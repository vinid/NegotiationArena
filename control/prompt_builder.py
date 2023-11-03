from typing import List

class Prompt:
    def __init__(self, prompt: List[str]):
        self.prompt = prompt
    
    def __str__(self):
        return '\n'.join(self.prompt)
        

class RulePrompt(Prompt):

    def __init__(self, rule: List[str]):
        self.rule = rule
        super().__init__(self.rule)
        

class GameRulesPrompt(Prompt):

     def __init__(self, prompts: List[Prompt]):
        self.prompts = prompts
        self.start_of_rule_prompt = "START OF THE RULES AND FORMATTING GUIDE.\n\n"
        self.end_of_rule_prompt = "\nEND OF THE RULES.\n"
        super().__init__(
            [self.start_of_rule_prompt] +\
            [str(i+1) + ") " + str(prompts[i]) + "\n" for i in range(len(self.prompts))] +\
            [self.end_of_rule_prompt]
        )





if __name__ == "__main__":
    pass