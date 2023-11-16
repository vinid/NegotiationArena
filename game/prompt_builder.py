from typing import List, Union

class Prompt:
    def __init__(self, prompt: List[str] = None):
        if prompt == None:
            prompt = []
        self.prompt = prompt
    
    def append(self, prompt: Union[List[str], str]):
        if isinstance(prompt,str):
            prompt = [prompt]
        self.prompt += prompt

    def __str__(self):
        return '\n'.join(self.prompt)
    
    def to_prompt(self):
        return self.__str__()

    def __add__(self, other):
        return Prompt(self.prompt + other.prompt)
        

class RulePrompt(Prompt):

    def __init__(self, rule: List[str]):
        self.rule = rule
        super().__init__(self.rule)
        

class GameRulesPrompt(Prompt):

     def __init__(self, prompts: List[Prompt]):
        self.prompts = prompts
        self.start_of_rule_prompt = "START OF THE FORMATTING GUIDE.\n"
        self.end_of_rule_prompt = "\nEND OF THE RULES.\n"
        super().__init__(
            [self.start_of_rule_prompt] +\
            [str(i+1) + ") " + str(prompts[i]) + "\n" for i in range(len(self.prompts))] +\
            [self.end_of_rule_prompt]
        )





if __name__ == "__main__":
    pass