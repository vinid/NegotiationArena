from typing import List

class Prompt:
    def __init__(self, prompt: List[str]):
        self.prompt = prompt
    
    def __str__(self):
        return '\n'.join(self.prompt)
    # def 


class RulePrompt(Prompt):

    def __init__(self, rule: List[str]):
        self.rule = rule
        super().__init__(self.rule)
        

class GameRulesPrompt(Prompt):

     def __init__(self, prompts: List[RulePrompt]):
        self.prompts = prompts
        self.start_of_rule_prompt = "START OF THE RULES AND FORMATTING GUIDE.\n\n"
        self.end_of_rule_prompt = "\nEND OF THE RULES.\n"
        super().__init__(
            [self.start_of_rule_prompt] +\
            [str(i+1) + ") " + str(prompts[i]) + "\n" for i in range(len(self.prompts))] +\
            [self.end_of_rule_prompt]
        )

class IntroductionPrompt(Prompt):
    def __init__(self, intro: List[str]):
        self.intro = intro
        super().__init__(self.intro)


class GamePrompt(Prompt):

    def __init__(self, prompts: List[Prompt]):
        self.prompts = prompts
        super().__init__(
           [str(prompts[i]) for i in range(len(self.prompts))]
        )

    


if __name__ == "__main__":
    a = RulePrompt([
        "This is the FINAL round of trading. So make sure to work your way up to the best possible trade.",
        "Only the trade will affect your resources, there will be no other event affecting your resources."
    ])
    b = RulePrompt([
        "Player 1 will suggest an initial trade like this:\n",
        "MY RESPONSE: NONE",
        "NEWLY PROPOSED TRADE: Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ..."
    ])

    c = RulePrompt([
        "When you receive a trade, you can either:\n",
        "Accept the trade by saying:",
        "MY RESPONSE: ACCEPTED",
        "NEWLY PROPOSED TRADE: NONE\n",
        "or reject the trade and you must propose a new trade:",
        "MY RESPONSE: REJECTED",
        "NEWLY PROPOSED TRADE: Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ...\n",
        "Note: the game will end if one of the players accepts.",
        "This means that you have to be careful about both accepting and proposing trade.",
        "If you feel like you are ok with the resources, don't want to share any or you want to buy time before deciding you have you can just keep rejecting offers and offer to exchange 0 resources, that is the same as offering nothing."
    ])


    rules = GameRulesPrompt([a,b,c])

    agent_context = Prompt([
        "Here is what you have access to:\n",
        "Potential Resources in the game: {}\n",
        "MY RESOURCES: {}",
        "MY GOAL: {}.\n",
        "Note, if you get less of each resource of your goal, you lose. You can have more if you want."
    ])
    
    
    
    intro = IntroductionPrompt([
        "You are playing a strategic game of trading resources with another player whose resources you have no knowledge about.",
        "Your main objective is to reach your goal.\n"
    ])


    z = GamePrompt([intro, rules, agent_context])
    print(z)

