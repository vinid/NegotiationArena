structured_calls = """You are playing a strategic game of trading resources with another player. 
You are playing against a player whose resources you have no knowledge about. 

You will respond one turn at a time. You can only accept one offer, so make sure the offer you accept is the one that 
allows you to win the game. You should only care about your resources and your goals, not much about the other player's.

You should start your messages by detailing the resources you own.
MY RESOURCES: item1: amount, item2: amount,...

There is a specific format you should follow to propose or accept a trade.

If you are Player 1, you will make an initial proposal in the following format:

NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, ... Player 2 Gives: item1: amount, item2: amount, ...

If it's your turn to respond, your response should be in the following format:

If you accept, do not propose a new offer, use the format:
PLAYER RESPONSE: ACCEPTED

if you reject, propose a new offer in the following format:
PLAYER RESPONSE: REJECTED
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount,  Player 2 Gives: item1: amount, item2: amount, ...

Game will finish after one of the player says:
PLAYER RESPONSE: ACCEPTED

Potential Resources in the Game: {}
Your Starting Resources: {}
Your goal: Finish the game with at least {}. Otherwise, you will lose the game. The games finishes when one of the players 
says PLAYER RESPONSE: ACCEPTED.

If you feel like you are ok with the resources you have you can just keep rejecting offers until the end of the game.

Remember you can only accept ONE time and then the game is over.
Think about this consideration everytime you want to accept a trade.
Reason step by step, but use the format to propose a trade. 
Reason step by step. Everytime you receive a trade, think if the trade lets you reach the goal, and consider previous proposals.
Reason step by step. Everytime you propose a trade, think if the trade lets you reach the goal, and consider previous proposals.

{}

{}
"""

asking_for_final_results = """The proposal was {0}. The game is over. I am the game master. Tell me the following:

          MY RESOURCES: (these are your original resources)
          {0} TRADE: (this is the trade that was {0})
          FINAL RESOURCES: (this is what you have after this trade) 
          """

