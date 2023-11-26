from ratbench.constants import *


def trading_prompt(
    resources_in_game,
    initial_resources,
    goal,
    number_of_proposals,
    social_behaviour,
):
    prompt = f"""You are playing a strategic game in which you are negotiating with another player on the price of an object. There is only one object for sale/purcahse.

A player is going to one object. The other player gives <{MONEY_TOKEN}> to buy resources.

RULES:

```
1. You can either:

A) Accept the trade by saying:
<{PLAYER_ANSWER_TAG}> ACCEPTED </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> NONE </{PROPOSED_TRADE_TAG}>

B) Reject and propose a new trade:
<{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> Player 1 Gives <item>: <amount, int>, Player 2 Gives <item>: <amount, int> . </{PROPOSED_TRADE_TAG}>

C) reject and wait for a new trade:\n
<{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> NONE </{PROPOSED_TRADE_TAG}>\n

Note: the game will end if one of the players accepts\n
This means that you have to be careful about both accepting and proposing a trade.

2. You are allowed at most {number_of_proposals} proposals of your own to complete the game, after which you can only ACCEPT or NONE.
DO NOT propose a new trade after {number_of_proposals} proposals. Your limit for proposals is {number_of_proposals}.

3. You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

4. At each turn send messages to each other by using the following format:
<{MESSAGE_TAG}>your message here</{MESSAGE_TAG}>
You can decide if you want disclose your resources and goals in the message.

5. Your goal is to negotiate with the other player.
```

Here is what you have access to:
```
<{OBJECT_TOKEN}> that is being bought/sold: {resources_in_game}
<{RESOURCES_TAG}> {initial_resources} </{RESOURCES_TAG}>
<{GOALS_TAG}> {goal} </{GOALS_TAG}>,
```

All the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
<{GOALS_TAG}> [add here] </{GOALS_TAG}>
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{MESSAGE_TAG}> [add here] </{MESSAGE_TAG}
<{PROPOSED_TRADE_TAG}> [add here] </{PROPOSED_TRADE_TAG}>
```

Please be sure to include all.

More resources in general are always better.

You objective is to negotiate for the best possible price for yourself.


{social_behaviour}
"""

    return prompt
