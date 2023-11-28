from typing import List, Union
from ratbench.constants import *


def ultimatum_prompt(
    player_1_initial_resources,
    player_2_initial_resources,
    player_1_reject_resources,
    resources_in_game,
    initial_resources,
    goal,
    number_of_proposals,
    social_behaviour,
):
    prompt = f"""You are playing a game involving a split of resources.  
    
Player 2 starts with {player_2_initial_resources}, Player 1 starts with no resources.

Player 1 has two options:
    Option A: Player 1 gains {player_1_reject_resources} and Player 2 loses everything.

    Option B: Player 2 has the free choice of how to split their resources with Player 1.

Player 

The game will follow this order exactly:
```

1. Player 1 makes a choice and responds with either:

    A) <{PLAYER_ANSWER_TAG}> OPTION_A </{PLAYER_ANSWER_TAG}>

    B) <{PLAYER_ANSWER_TAG}> OPTION_B </{PLAYER_ANSWER_TAG}>
    
2. If Player 1 chooses Option B, Player 2 will know this and can split his resource in any way he wants:

    <{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
    <{SPLIT_TAG}> Player 1 Gives {', '.join([k+" : 0" for k in resources_in_game.keys()])}, Player 2 Gives {', '.join([k+": [add here]"for idx, k in enumerate(resources_in_game.keys())])}</{SPLIT_TAG}>

3. The game ends immeditely after Player 2 makes their proposal. There are no more future games.
```

You can reason step by step on why you are A) proposing, B) Accepting and C) Rejecting a trade with:
<{REASONING_TAG}> [add reasoning] </{REASONING_TAG}>. add as much text as you want
This information will not be sent to the other player. It is just for you to keep track of your reasoning.


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
<{SPLIT_TAG}> NONE </{SPLIT_TAG}>
```

If you are Player 2 all the responses you send should contain the following and in this order:

```
<{RESOURCES_TAG}> [add here] </{RESOURCES_TAG}
<{REASONING_TAG}> [add here] </{REASONING_TAG}>
<{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
<{SPLIT_TAG}> Player 1 Gives {', '.join([k+" : 0" for k in resources_in_game.keys()])}, Player 2 Gives {', '.join([k+": [add here]"for idx, k in enumerate(resources_in_game.keys())])}</{SPLIT_TAG}>

Please be sure to include all.

{social_behaviour}
"""

    return prompt
