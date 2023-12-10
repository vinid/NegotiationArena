from typing import List, Union
from ratbench.constants import *


# If you do reach an agreement on how to split the resources, you both lose all the resources.
# Player 1 stars with all the resources, Player 2 has none to trade.
# All the trades will involve what Player 1 is going to give to Player 2.


def ultimatum_prompt(
    player_1_initial_resources,
    resources_in_game,
    initial_resources,
    social_behaviour,
):
    prompt = f"""You are playing a game involving a split of resources. 
{AGENT_ONE} stars with {player_1_initial_resources}, {AGENT_TWO} has none to trade.

RULES:
```
1.  Each player only has one move.

2.  {AGENT_ONE} proposes a split of how much {AGENT_ONE} gives to {AGENT_TWO}:

    <{PLAYER_ANSWER_TAG}> WAIT </{PLAYER_ANSWER_TAG}>
    <{PROPOSED_TRADE_TAG}> {AGENT_ONE} Gives {', '.join([k+": amount"+str(idx) for idx, k in enumerate(resources_in_game.keys())])} | {AGENT_TWO} Gives {', '.join([k+" : 0" for k in resources_in_game.keys()])} </{PROPOSED_TRADE_TAG}>

3.  {AGENT_ONE} cannot propose a trade. {AGENT_TWO} can only either:

    A) Accept the trade by saying:
    <{PLAYER_ANSWER_TAG}> {ACCEPTING_TAG} </{PLAYER_ANSWER_TAG}>

    B) Reject by saying:
    <{PLAYER_ANSWER_TAG}> {REJECTION_TAG} </{PLAYER_ANSWER_TAG}>
  
4. If {AGENT_TWO} Accepts, the trade proceeds. If {AGENT_TWO} Rejects, both players lose all resources.

5. The game is over after {AGENT_TWO} Accepts or Rejects.

6. You can reason step by step on why you are A) proposing, B) rejecting and C) accepting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}> add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

```

Here is what you have access to:
```
Resources available in the game: {resources_in_game.keys()}
<{RESOURCES_TAG}> {initial_resources} </{RESOURCES_TAG}>
```

If you are {AGENT_ONE}, all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> [add here] </{PROPOSED_TRADE_TAG}>
```

If you are {AGENT_TWO} all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}>
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> [add here] </{PLAYER_ANSWER_TAG}>
<{PROPOSED_TRADE_TAG}> NONE </{PROPOSED_TRADE_TAG}>

Please be sure to include all.

Note, if you don't find an agreement, you both don't get anything.



{social_behaviour}
"""

    return prompt
