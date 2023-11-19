from game.constants import *


def trading_prompt(
    resources_in_game,
    initial_resources,
    valuation,
    goal,
    number_of_proposals,
    social_behaviour,
):
    prompt = f"""You are playing a strategic game in which you are negotiating with another player on the price of a object.Player 1 is going to sell resources. Player 2 gives <{MONEY_TOKEN}> to buy resources.

RULES:

```
Player 1 will suggest an initial trade:

f"<{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>",
f"<{PROPOSED_TRADE_TAG}> Player 1 Gives <{OBJECT_TOKEN}>: 1, Player 2 Gives {MONEY_TOKEN}: amount </{PROPOSED_TRADE_TAG}>

A) Accept the trade by saying:
<{PLAYER_ANSWER_TAG}> ACCEPTED </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>

B) Reject and propose a new trade:
<{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> Player 1 Gives <{OBJECT_TOKEN}>: 1, Player 2 Gives {MONEY_TOKEN}: amount . </{PROPOSED_TRADE_TAG}>

C) reject and wait for a new trade:\n
<{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>\n

Note: the game will end if one of the players accepts\n
This means that you have to be careful about both accepting and proposing a trade.

You are allowed at most {number_of_proposals} proposals of your own to complete the game, after which you can only ACCEPT or WAIT.
DO NOT propose a new trade after {number_of_proposals} proposals.

You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

At each turn send messages to each other by using the following format:
<{MESSAGE_TAG}>your message here</{MESSAGE_TAG}>
You can decide if you want disclose your resources and goals in the message.

Your goal is to negotiate with the other player.
```

Here is what you have access to:
```
 Here is what you have access to:
f" <{OBJECT_TOKEN}> that is being bought/sold: {resources_in_game}
f"<{RESOURCES_TAG}> {initial_resources} </{RESOURCES_TAG}>
f"<{VALUATION_TAG}> {valuation} </{VALUATION_TAG}> refers to how much you value resources in terms of {MONEY_TOKEN}
f"<{GOALS_TAG}> {goal} </{GOALS_TAG}>\n",
```

All the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
<{GOALS_TAG}> [add here] </{GOALS_TAG}>
<{VALUATION_TAG}> [add here] </{VALUATION_TAG}>
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{MESSAGE_TAG}> [add here] </{MESSAGE_TAG}
<{PROPOSED_TRADE_TAG}> [add here] </{PROPOSED_TRADE_TAG}>
```

Please be sure to include all.

More resources in general are always better.


{social_behaviour}
"""

    return prompt
