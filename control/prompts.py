structured_calls = """
You are playing a strategic game of trading resources with another player whose resources you have no knowledge about.
Your main objective is to reach your goal.

START OF THE RULES AND FORMATTING GUIDE.

Only the trade will affect your resources, there will be no other event affecting your resources.

1) Player 1 will suggest an initial trade like this:

<response> WAIT </response>
<newly proposed trade> Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ... </newly proposed trade>

2) When you receive a trade, you can either:

Accept the trade by saying:
<response> ACCEPTED </response>
<newly proposed trade> WAIT </newly proposed trade>

or reject and ignore the trade. When you reject you can propose a new trade:
<response> WAIT </response>
<newly proposed trade> Player 1 Gives item1: amount, item2: amount, Player 2 Gives item1: amount, item2: amount, ... </newly proposed trade>

or not:
<response> WAIT </response>
<newly proposed trade> WAIT </newly proposed trade>

Note: the game will end if one of the players accepts. This means that you have to be careful about both accepting and proposing trade.  

3) You can reason step by step on why you are A) proposing, B) rejecting or C) accepting a trade with:
<reason> [add reasoning] </reason>
This information will not be sent to the other player. It is just for you to keep track of your reasoning.

4) At each turn send messages to each other by using the following format:
<message>your message here</message>
You can decide if you want disclose your resources and goals in the message.

END OF THE RULES.

Here is what you have access to: 

Potential Resources in the game: {}

<my resources> {} </my resources>
<my goal> {} </my goal> 

Note, if you get less of each resource of your goal, you lose. You can have more if you want. 

All the messages you send should contain the following and in this order. 

``` 
<my resources> add here </my resources>
<my goal> my goal </my goal> 
<my response> [add here] </my response>
<reason> [add here] </reason>
<message> [add here] </message>
<newly proposed trade>[add here] </newly proposed trade>
```
Please be sure to include all.

{}

{}

"""

asking_for_final_results = """The proposal was {0}. The game is over. I am the game master. Tell me the following:

          <my resources> (these are your original resources) </my resources>
          <{0} trade> (this is the trade that was {0}) </{0} trade>
          <final resources> (this is what you have after this trade) </final resources> 
          follow this formatting, do not add newlines where not needed.
          """

