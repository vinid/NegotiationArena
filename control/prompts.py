structured_calls = """
You are playing a strategic game of trading resources with another player. 
You are playing against a player whose resources you have no knowledge about. 

Follow these guidelines and formatting instructions: 

START OF THE RULES.

1) This is the last round of trading. So make sure to work your way up to the best possible trade.
Only the trade will affect your resources, there will be no other event affecting your resources.

2) Player 1 will suggest an initial trade in the following format:

PLAYER RESPONSE: NONE
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, Player 2 Gives: item1: amount, item2: amount, ...
Note that amounts are integers.

3) When you receive a trade, you can either accept or reject it and propose a new trade.

If you accept, do not propose a new offer, just say:
PLAYER RESPONSE: ACCEPTED

The game will finish if one of the players accepts. This means that you have to be careful about accepting a trade.  
Acceptance will happen once and then the game will be over.

4) if you reject, you must propose a new trade, say:
PLAYER RESPONSE: REJECTED
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, Player 2 Gives: item1: amount, item2: amount, ...

If you feel like you are ok with the resources or you want to buy time before deciding you have you can just keep rejecting offers and offer to exchange 0 resources, that is the same as offering nothing.

5) You can reason step by step why you are proposing, rejecting or accepting a trade with:
REASON: your reasoning here

This information will be kept private.

6) At each turn send messages to each other by using the following format:
MESSAGE: your message here
You can decide if you want disclose your resources and goals.

END OF THE RULES.

Here is what you have access to: 

Potential Resources in the game: {}

MY RESOURCES: {}
MY GOAL: {}. 

Note, if you get less of each resource of your goal, you lose. You can have more if you want. 

All the messages you send should contain the following and in this order:

``` 
MY RESOURCES:
MY GOAL:
PLAYER RESPONSE:
REASON:
MESSAGE:
NEWLY PROPOSED TRADE:
```
Please be sure to include all.
 
{}

{}


"""

asking_for_final_results = """The proposal was {0}. The game is over. I am the game master. Tell me the following:

          MY RESOURCES: (these are your original resources)
          {0} TRADE: (this is the trade that was {0})
          FINAL RESOURCES: (this is what you have after this trade) 
          follow this formatting, do not add newlines where not needed.
          """

