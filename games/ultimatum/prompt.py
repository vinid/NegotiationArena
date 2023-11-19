from typing import List, Union
from game.constants import *

def ultimatum_prompt(
    resources_in_game, initial_resources, goal, number_of_proposals, social_behaviour
):
    prompt = f"""You are playing a strategic game in which you need to split resources with another player. 
If you do not find a way to reach an agreement on how to split the resources, you both lose all the resources.
Player 1 stars with all the resources, Player 2 has none to trade. 
All the trades will involve what Player 1 is going to give to Player 2.

RULES:
```

1. You can either:

A) Accept the trade by saying:
<{PLAYER_ANSWER_TAG}> ACCEPTED </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>

B) Reject and propose a new trade:
<{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> Player 1 Gives item1: amount, Player 2 Gives item1: 0 </{PROPOSED_TRADE_TAG}>

C) Reject and wait for a new trade:\n
<{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>\n

Note: the game will end if one of the players accepts\n
This means that you have to be careful about both accepting and proposing a trade.

2. You are allowed at most {number_of_proposals} proposals of your own to complete the game, after which you can only ACCEPT or WAIT.
DO NOT propose a new trade after {number_of_proposals} proposals. Your limit for proposals is {number_of_proposals}.

3. You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

4. At each turn send messages to each other by using the following format:
<{MESSAGE_TAG}>your message here</{MESSAGE_TAG}>
You can decide if you want disclose your resources and goals in the message.

5. Your goal is to meet your objectives immediately, this is the last round of trading.
```

Here is what you have access to:
```
Resources available in the game: {resources_in_game}
<{RESOURCES_TAG}> {initial_resources} </{RESOURCES_TAG}>
<{GOALS_TAG}> {goal} </{GOALS_TAG}>
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

Note, if you don't find an agreement, you both don't get anything.



{social_behaviour}
"""

    return prompt
