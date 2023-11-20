from typing import List, Union
from game.constants import *


# If you do reach an agreement on how to split the resources, you both lose all the resources.
# Player 1 stars with all the resources, Player 2 has none to trade.
# All the trades will involve what Player 1 is going to give to Player 2.


def ultimatum_prompt(
    resources_in_game, initial_resources, goal, number_of_proposals, social_behaviour
):
    prompt = f"""You are playing a strategic game in which you need to split resources with another player. 

RULES:
```

1.  Player 1 proposes a split of resources with the command:

    <{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
    <{PROPOSED_TRADE_TAG}> Player 1 Gives item1: amount, Player 2 Gives item1: 0 </{PROPOSED_TRADE_TAG}>

2.  Player 2 can either:

    A) Accept the trade by saying:
    <{PLAYER_ANSWER_TAG}> ACCEPTED </{PLAYER_ANSWER_TAG}>
    <{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>

    B) Reject:
    <{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
  
3. If Player 2 Accepts, the trade is proceeded. If Player 2 Rejects both players lose all resources.

4. The game is over after Player 2 Accepts or Rejects.

5. You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

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
