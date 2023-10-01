structured_calls = """You are playing a strategic game of trading resources with another player. You are Player 1. You are playing against a player whose resources you have no knowledge about.

You will respond one turn at a time. At each step, you will state your current resources and either propose or respond to a trade.
If it's your turn to propose, your response should be in the following format:

RESOURCES: item1: amount, item2: amount, ... # Your resources

PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, ... Player 2 Gives: item1: amount, item2: amount, ...

and do not say anything else. If it's your turn to respond, your response should be in the following format:

PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount, ... Player 2 Gives: item1: amount, item2: amount, ...
PLAYER RESPONSE: {{ACCEPTED/REJECTED}}
RESOURCES AFTER TRADE: item1: amount, item2: amount, ... # Your resources
NEWLY PROPOSED TRADE: Player 1 Gives: item1: amount, item2: amount,  Player 2 Gives: item1: amount, item2: amount, ...

and again, do not say anything else.

Potential Resources in the Game: {}
Your Starting Resources: {}
Your goal: Finish the game with at least {} in under {} rounds of proposals. Otherwise, you will die.

{}
"""



