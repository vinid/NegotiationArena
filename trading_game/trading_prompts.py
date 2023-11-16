from game.constants import *
from game.prompt_builder import Prompt, GameRulesPrompt


## Introduction
intro = Prompt([
    "You are playing a strategic game of trading resources with another player whose resources you have no knowledge about.",
    "",
])

## Rules
initial_trade_rule = Prompt([
    "Player 1 will suggest an initial trade:\n",
    f"<{PLAYER_RESPONSE_TAG}> WAIT </{PLAYER_RESPONSE_TAG}>",
    f"<{PROPOSED_TRADE_TAG}> Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ... </{PROPOSED_TRADE_TAG}>"
])

response_trade_rule = Prompt([
    "When you receive a trade, you can either:\n",
    "A) Accept the trade by saying:",
    f"<{PLAYER_RESPONSE_TAG}> ACCEPTED </{PLAYER_RESPONSE_TAG}>"
    f"<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>\n",
    "B) Reject and propose a new trade:\n",
    f"<{PLAYER_RESPONSE_TAG}> WAIT </{PLAYER_RESPONSE_TAG}>",
    f"<{PROPOSED_TRADE_TAG}> Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ... </{PROPOSED_TRADE_TAG}>\n"
    # "C) reject and wait for a new trade:\n",
    # f"<{PLAYER_RESPONSE_TAG}> WAIT </{PLAYER_RESPONSE_TAG}>",
    # f"<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>\n",
    "Note: the game will end if one of the players accepts\n",
    "This means that you have to be careful about both accepting and proposing a trade."
])

reasoning_rule = Prompt([
    "You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:",
    f"<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> "
    f"add as much text as you want",
    "This information will not be sent to the other player. It is just for you to keep track of your reasoning."
])

messaging_rule = Prompt([
    "At each turn send messages to each other by using the following format:",
    f"<{MESSAGE_TAG}>your message here</{MESSAGE_TAG}>"
    "You can decide if you want disclose your resources and goals in the message."
])

rules = GameRulesPrompt([
    initial_trade_rule,
    response_trade_rule,
    reasoning_rule,
    # messaging_rule
])


agent_objective = Prompt([
    "Your goal is to meet your objectives immediately, this is the last round of trading.\n"
])

# Agent Context
class AgentContextPrompt(Prompt):
    """
    Prompt for inital agent context
    """

    def __init__(self, potential_resources, agent_initial_resources, agent_goal):
        self.prompts = [
            "Here is what you have access to:\n",
            f"Resources available in the game: {potential_resources.to_prompt()}\n"
            f"<{RESOURCES_TAG}> {agent_initial_resources.to_prompt()} </{RESOURCES_TAG}>"
            f"<{GOALS_TAG}> {agent_goal.to_prompt()} </{GOALS_TAG}>\n",
            "Note, if you get less of each resource of your goal, you lose.\n",
            "More resources in general are always better.\n",
            "You should win the game immediately\n"
        ]
        super().__init__(
            [str(self.prompts[i]) for i in range(len(self.prompts))]
        )


## Number of rounds
class RoundsPrompt(Prompt):
    def __init__(self, n_rounds: int):
        self.prompts = [
            "\nYou have at most {} proposals to complete the game.".format(n_rounds)
        ]

        super().__init__(
            [str(p) for p in self.prompts]
        )


class NegotiationPrompt(Prompt):
    def __init__(self,
                 potential_resources,
                 agent_initial_resources,
                 agent_goal,
                 n_rounds,
                 agent_social_behaviour):
        self.prompts = [
            intro,
            rules,
            AgentContextPrompt(potential_resources, agent_initial_resources, agent_goal),
            RoundsPrompt(n_rounds),
            Prompt(['', agent_social_behaviour]),
            agent_objective
        ]

        super().__init__(
            [str(self.prompts[i]) for i in range(len(self.prompts))]
        )
