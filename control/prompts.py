structured_calls = """You are playing a strategic game of trading resources with another player. 
You are playing against a player whose resources you have no knowledge about. 

You will respond one turn at a time. 
This is the last round of trading. So make sure to reach the goal by the end of it.
You can decide if you want disclose your resources and goals.
Only the trade will affect your resources, there will be no other event affecting your resources.

Follow these guidelines. There is a format to follow: 

1) You should start your messages by detailing the resources you own and your goal.
MY RESOURCES: item1: amount, item2: amount,...
MY GOAL: item1: amount, item2: amount,...

2) If you are Player 1, you can make an initial proposal in the following format:

NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, Player 2 Gives: item1: amount, item2: amount, ...
Note that amounts are integers.

3) If it's your turn to respond, your response should be in the following format:

If you accept, do not propose a new offer, use the format:
PLAYER RESPONSE: ACCEPTED

4) if you reject, you must propose a new trade in the following format:
PLAYER RESPONSE: REJECTED
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, Player 2 Gives: item1: amount, item2: amount, ...

5) To explain your reasoning, you can use the following format:
REASON: your reasoning here
1) Reason step by step: does the offer you are going to make makes you win?
2) Reason step by step: does the offer that the other player made makes you win?

This REASON information will not be sent to the other player, it is just for you to keep track of your reasoning.

6) At each turn send messages to each other by using the following format:
MESSAGE: your message here

7) Game will finish after one of the players say:
PLAYER RESPONSE: ACCEPTED
If you feel like you are ok with the resources or you want to buy time before deciding you have you can just keep rejecting offers and offer to exchange 0 resources, that is the same as offering nothing.

8) You can only accept ONE time and then the game is over; the same is true for the other player. 
Remember, if you make a suboptimal trade and the other player accepts, the game is over. Propose trades that make you win.

End of the rules. Here is what you have: 

Potential Resources in the Game: {}


MY RESOURCES: {}
MY GOAL: Finish the game with at least {}. 
If you get less of each resource, you lose. 

You can only use the commands. Do not use other words. 

MY RESOURCES
MY GOAL
NEWLY PROPOSED TRADE
PLAYER RESPONSE
REASON
MESSAGE

This is the last trade round. If you accept, the game is over. 
 

{}

{}


"""

asking_for_final_results = """The proposal was {0}. The game is over. I am the game master. Tell me the following:

          MY RESOURCES: (these are your original resources)
          {0} TRADE: (this is the trade that was {0})
          FINAL RESOURCES: (this is what you have after this trade) 
          follow this formatting, do not add newlines where not needed.
          """

