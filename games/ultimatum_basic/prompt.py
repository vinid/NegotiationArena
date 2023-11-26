from typing import List, Union
from ratbench.constants import *


# If you do reach an agreement on how to split the resources, you both lose all the resources.
# Player 1 stars with all the resources, Player 2 has none to trade.
# All the trades will involve what Player 1 is going to give to Player 2.


def ultimatum_prompt(
    player_1_initial_resources,
    resources_in_game,
    initial_resources,
    goal,
    number_of_proposals,
    social_behaviour,
):
    prompt = f"""You are playing a game involving a split of resources. 
    Player 1 stars with {player_1_initial_resources} Player 2 has none to trade.

RULES:
```
1.  Each player only has one move.

2.  Player 1 proposes a split of how much Player 1 gives to Player 2:

    <{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
    <{PROPOSED_TRADE_TAG}> Player 1 Gives {resources_in_game.keys()[0]}: amount, Player 2 Gives {resources_in_game.keys()[0]}: 0 </{PROPOSED_TRADE_TAG}>

3.  Player 2 cannnot propose a trade. Player 2 can only either:

    A) Accept the trade by saying:
    <{PLAYER_ANSWER_TAG}> ACCEPTED </{PLAYER_ANSWER_TAG}>

    B) Reject by saying:
    <{PLAYER_ANSWER_TAG}> REJECT </{PLAYER_ANSWER_TAG}>
  
4. If Player 2 Accepts, the trade proceeds. If Player 2 Rejects, both players lose all resources.

5. The game is over after Player 2 Accepts or Rejects.

6. You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

```

Here is what you have access to:
```
Resources available in the game: {resources_in_game.keys()}
<{RESOURCES_TAG}> {initial_resources} </{RESOURCES_TAG}>
```

IF you are Player 1, all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> [add here] </{PROPOSED_TRADE_TAG}>
```

IF you are Player 12 all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> WAIT </{PROPOSED_TRADE_TAG}>

Please be sure to include all.

Note, if you don't find an agreement, you both don't get anything.



{social_behaviour}
"""

    return prompt
