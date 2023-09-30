initial_prompt = """
You are playing a game.

{resources}.

{goal}. 

You must obtain these resources by the end of the negotiation. You would lose with any less. 

You might already have some of the resources needed. You don't have other resources.

You need to negotiate with the other player. You don't know what the player has, and the player doesn't know what you have.

You will interact one turn at a time. Don't prepend anything to the offer.

If you don't get the required items by the end of the negotiation, you lose. 

You do not need to share any information regarding the resources you have. You are allowed to not disclose this.

This is your only chance of negotiating with the other player. When you are done negotiating just write DONE.
"""
