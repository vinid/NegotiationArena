structured_calls = """
You are playing a strategic game of trading resources with another player whose resources you have no knowledge about.  

START OF THE RULES AND FORMATTING GUIDE.

1) This is the last round of trading. So make sure to work your way up to the best possible trade.
Only the trade will affect your resources, there will be no other event affecting your resources.

2) Player 1 will suggest an initial trade like this:

MY RESPONSE: NONE
NEWLY PROPOSED TRADE: Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ...

3) When you receive a trade, you can either:

Accept the trade by saying:
MY RESPONSE: ACCEPTED
NEWLY PROPOSED TRADE: NONE

or reject the trade and you must propose a new trade:
MY RESPONSE: REJECTED
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, Player 2 Gives: item1: amount, item2: amount, ...

Note: the game will end if one of the players accepts. 
This means that you have to be careful about accepting a trade.  
If you feel like you are ok with the resources, don't want to share any or you want to buy time before deciding you have you can just keep rejecting offers and offer to exchange 0 resources, that is the same as offering nothing.

5) You can reason on why you are A) proposing, B) rejecting or C) accepting a trade with:
REASON: [add reasoning]
follow this format: I will reject the other player's trade because giving N of these resources... [do the math here]. I will propose to trade N of this resources for...[do the math here]. I will accept the other player's trade because if I get N of these resources...[do the math here].

This information will not be sent to the other player. It is just for you to keep track of your reasoning.

6) At each turn send messages to each other by using the following format:
MESSAGE: your message here
You can decide if you want disclose your resources and goals in the message.

END OF THE RULES.

Here is what you have access to: 

Potential Resources in the game: {}

MY RESOURCES: {}
MY GOAL: {}. 

Note, if you get less of each resource of your goal, you lose. You can have more if you want. 

All the messages you send should contain the following and in this order. Don't go to newline after a command.

``` 
MY RESOURCES: [add here]
MY GOAL: [add here]
MY RESPONSE: [add here]
REASON: [add here]
MESSAGE: [add here]
NEWLY PROPOSED TRADE: [add here]
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

