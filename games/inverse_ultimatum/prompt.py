from typing import List, Union
from ratbench.constants import *


# If you do reach an agreement on how to split the resources, you both lose all the resources.
# Player 1 stars with all the resources, Player 2 has none to trade.
# All the trades will involve what Player 1 is going to give to Player 2.


def ultimatum_prompt(
    player_1_initial_resources,
    player_2_initial_resources,
    resources_in_game,
    initial_resources,
    goal,
    number_of_proposals,
    social_behaviour,
):
    prompt = f"""You are playing a game involving a split of Player 2 resources. 
    In this game, the decision to accept or reject a split is made by Player 1 of BEFORE Player 2 proposes the split.
    After Player 2 proposes the split, Player 1 can no longer accept or reject.

RULES:
```

<Player 1 RESOURCES> {player_1_initial_resources} </Player 1 RESOURCES> 
<Player 2 RESOURCES> {player_2_initial_resources} </Player 2 RESOURCES>

1.  Each player only has one move.

2.  Player 1 decides whether to accept or reject Player 2's split before Player 2 proposes it. 
    This decision is final and cannot be changed through the rest of the game. It will apply to the next trade which Player 1 proposes.
    This is Player 1's only available action.
    
    Player 1 responds with either:

    A) Accept:
    <{PLAYER_ANSWER_TAG}> ACCEPTED </{PLAYER_ANSWER_TAG}>

    B) Reject:
    <{PLAYER_ANSWER_TAG}> REJECTED </{PLAYER_ANSWER_TAG}>
    
3. If Player 1 Accepts, the trade future Player 2 will propose will proceed. 
   

4. If Player 1 Rejects, Player 2 will lose all their resources and Player 1 will be given an additional {resources_in_game.keys()[0]}: 20 and the game ends.

5.  Player 2 then proposes a split of how much to give Player 2 based on Player 1 decision in Step 2.:

    <{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
    <{PROPOSED_TRADE_TAG}> Player 1 Gives {', '.join([k+" : 0" for k in resources_in_game.keys()])}, Player 2 Gives {', '.join([k+": amount"+str(idx) for idx, k in enumerate(resources_in_game.keys())])}</{PROPOSED_TRADE_TAG}>

6. The game ends immeditely after Player 2 makes their proposal.

7. There are no more future games.

8. You can reason step by step on why you are A) proposing, B) Accepting and C) Rejecting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}>. add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

```

Here is what you have access to:
```
Resources available in the game: {resources_in_game.keys()}
<{RESOURCES_TAG}> {initial_resources} </{RESOURCES_TAG}>
```

IF you are Player 1, all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] [not available to Player 2] </{RESOURCES_TAG}>
<{REASONING_TAG}> [add here] [not available to Player 2] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> NONE </{PROPOSED_TRADE_TAG}>
```

If you are Player 2 all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] [not available to Player 1]  </{RESOURCES_TAG}
<{REASONING_TAG}> [add here] [not available to Player 1]  </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> [add here] </{PROPOSED_TRADE_TAG}>

Please be sure to include all.

Note, if you don't find an agreement, you both don't get anything.



{social_behaviour}
"""

    return prompt


""""<Player 1 RESOURCES> [add here] </Player 1 RESOURCES>
<ACCEPTED rule> [add here] </ACCEPTED rule>
<REJECTED rule> [add here] </REJECTED rule>"""
