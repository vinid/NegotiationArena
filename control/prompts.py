from control.prompt_builder import Prompt, RulePrompt, GameRulesPrompt


## Introduction
intro = Prompt([
        "You are playing a strategic game of trading resources with another player whose resources you have no knowledge about.",
        "Your main objective is to reach your goal.\n"
    ])

## Rules
initial_trade_rule = Prompt([
    "Player 1 will suggest an initial trade:\n",
    "<my response> WAIT </my response>",
    "<newly proposed trade> Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ... </newly proposed trade>"
])

response_trade_rule = Prompt([
    "When you receive a trade, you can either:\n",
    "A) Accept the trade by saying:",
    "<my response> ACCEPTED </my response>"
    "<newly proposed trade> WAIT </newly proposed trade>\n",
    "B) Reject and propose a new trade:\n",
    "<my response> WAIT </my response>",
    "<newly proposed trade> Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ... </newly proposed trade>\n"
    "C) reject and wait for a new trade:\n",
    "<my response> WAIT </my response>",
    "<newly proposed trade> WAIT </newly proposed trade>\n",
    "Note: the game will end if one of the players accepts\n",
    "This means that you have to be careful about both accepting and proposing a trade."
])

reasoning_rule = Prompt([
    "You can reason step by step on why you are A) proposing, B) rejecting or C) accepting a trade with:",
    "<reason> [add reasoning] </reason>",
    "This information will not be sent to the other player. It is just for you to keep track of your reasoning."
])

messaging_rule = Prompt([
    "At each turn send messages to each other by using the following format:",
    "<my message>your message here</my message>"
    "You can decide if you want disclose your resources and goals in the message."
])


rules = GameRulesPrompt([
    initial_trade_rule,
    response_trade_rule,
    reasoning_rule,
    messaging_rule
])

# Agent Context
class AgentContextPrompt(Prompt):
    """
    Prompt for inital agent context
    """
    
    def __init__(self, potential_resources, agent_initial_resources, agent_goal):
        self.prompts = [
            "Here is what you have access to:\n",
            "Resources available in the game: {}\n".format(potential_resources),
            "<my resources> {} </my resources>".format(agent_initial_resources),
            "<my goal> {} </my goal>\n".format(agent_goal),
            "Note, if you get less of each resource of your goal, you lose.\n", 
            "More resources in general are always better.\n"
        ]
        super().__init__(
           [str(self.prompts[i]) for i in range(len(self.prompts))]
        )

## Response Formatting
response_format = Prompt([
    "All the responses you send should contain the following and in this order.\n"
    "```",
    "<my resources> [add here] </my resources>",
    "<my goal> [add here] </my goal>",
    "<reason> [add here] </reason>",
    "<my response> [add here] </my response>",
    "<my message> [add here] </my message>",
    "<newly proposed trade> [add here] </newly proposed trade>",
    "```",
    "Please be sure to include all."
])


## Number of rounds
class RoundsPrompt(Prompt):
    def __init__(self, n_rounds: int):
        self.prompts = [
           "\nYou have at most {} proposals to complete the game.".format(n_rounds)
        ]

        super().__init__(
           [str(p) for p in self.prompts]
        )


# Overall Prompt
class TradingGame(Prompt):
    
    def __init__(self, 
                potential_resources, 
                agent_initial_resources,
                agent_goal,
                n_rounds,
                agent_social_behaviour):
        self.prompts = [
            intro, 
            rules, 
            AgentContextPrompt(potential_resources, agent_initial_resources, agent_goal ),
            response_format,
            RoundsPrompt(n_rounds),
            Prompt(['',agent_social_behaviour])
        ]

        super().__init__(
           [str(self.prompts[i]) for i in range(len(self.prompts))]
        )

asking_for_final_results = """The proposal was {0}. The game is over. I am the game master. Tell me the following:

          <my resources> (these are your original resources) </my resources>
          <{0} trade> (this is the trade that was {0}) </{0} trade>
          <final resources> (this is what you have after this trade) </final resources> 
          follow this formatting, do not add newlines where not needed.
          """

