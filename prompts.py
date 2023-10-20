structured_calls = """You are playing a strategic game of trading resources with another player. 
You are playing against a player whose resources you have no knowledge about. 

You will respond one turn at a time. You can only accept one offer, so make sure the offer you accept is the one that 
allows you to win the game.

If you are Player 1, you will start by making a proposal in the following format:

PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, ... Player 2 Gives: item1: amount, item2: amount, ...

and do not say anything else. 

If it's your turn to respond, your response should be in the following format:

If you accept, do not propose a new offer, use the format:
PLAYER RESPONSE: ACCEPTED

if you reject, propose a new offer in the following format:
PLAYER RESPONSE: REJECTED
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount,  Player 2 Gives: item1: amount, item2: amount, ...

and again, do not say anything else. Game will finish after one of the player says:
PLAYER RESPONSE: ACCEPTED

Potential Resources in the Game: {}
Your Starting Resources: {}
Your goal: Finish the game with at least {} in under {} rounds of proposals. Otherwise, you will lose the game.

{}
"""



