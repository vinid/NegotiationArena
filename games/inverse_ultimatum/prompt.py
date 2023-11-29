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
    prompt = f"""You are playing a game involving a split of resources. The goal is to maximize your resources.
    
Player 1 starts with no resources, Player 2 starts with {player_2_initial_resources}.

There are two turns in this game.

Player 1 makes a decison first. This is shared with Player 2, who then chooses a split.


Turn 1: 
```
    Player 1 has two options:

        Option A: Player 1 gains {player_1_reject_resources} and Player 2 loses everything.

        Option B: Playser 1 does not gain {player_1_reject_resources}. Player 2 does not lose everything. Player 2 has the free choice of how to split their resources with Player 1.

        Note the following:
            - Player 2 cannot be influenced in any way since he makes his split after Player 1 chooses
            - Player 2 will only lose all his resources if Player 1 chooses Option A. This does not happen for Option B. 
            - Player 2 has not made any split porposal yet.

    Player 1 makes a choice and responds with either:

        A) <{PLAYER_ANSWER_TAG}> OPTION_A </{PLAYER_ANSWER_TAG}>

        B) <{PLAYER_ANSWER_TAG}> OPTION_B </{PLAYER_ANSWER_TAG}>            
```

Turn 2:
```
    Turn 2 only occurs if Player 1 choses OPTION_B. Player 2 will not lose anything.

    Player 2 can split his resources in any way he wants. Player 2 does not need Player 1's approval.

    Player 2 should respond in this format:

        <{PLAYER_ANSWER_TAG}> NONE </{PLAYER_ANSWER_TAG}>
        <{SPLIT_TAG}> Player 1 Gives {', '.join([k+" : 0" for k in resources_in_game.keys()])}, Player 2 Gives {', '.join([k+": amount"for idx, k in enumerate(resources_in_game.keys())])}</{SPLIT_TAG}>

    Note: Use "Gives" and not "Gets" in your reply.
```

There are no future games, but you should aim to win this game.

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
<{SPLIT_TAG}> [add here] </{SPLIT_TAG}>

Please be sure to include all.

{social_behaviour}
"""

    return prompt
