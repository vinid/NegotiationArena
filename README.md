# How Well Can LLMs Negotiate? The NegotiationArena Platform and Analysis

## Experiments

Experiments are available in the `experiments` folder. There is one running file for
each game we have run. 

If you want to recreate the plots, you can look at the notebook and analysis folders. You will find a way
to load all the games in one batch and then run the analysis on them.

The log files store the entire logs. We have also saved the broken games in the logs_error folders
in case you want to look at them.


### Using The WebApp

You can load the webapp by running the following command:

```bash
streamlit run app.py
```

The webapp is found under the `explorer` folder. It is a simple interface to load games and 
explore them and provides barebones support, but it's pretty good to get a quick overview of the
results of the games.

## Running Games

Running and modifying a game is relatively easy. This is for example the
main interface used to run a BuySellGame.

```python

a1 = ChatGPTAgent(agent_name="Player 1", model="gpt-4-1106-preview")
a2 = ChatGPTAgent(agent_name="Player 2", model="gpt-4-1106-preview")

c = BuySellGame(players=[a1, a2],
    iterations=10,
    resources_support_set=Resources({"X": 0}),
    player_goals=[
        SellerGoal(cost_of_production=Valuation({"X": 40})),
        BuyerGoal(willingness_to_pay=Valuation({"X": 20})),
    ],
    player_initial_resources=[
        Resources({"X": 1}),
        Resources({MONEY_TOKEN: 100}),
    ],
    player_roles=[
        "You are Player 1.",
        "You are Player 2.",
    ],
    player_social_behaviour=[
        "",
        "you care only about your goals",  # sound angry. do not try to find middle ground. care only about yourself",
    ],
    log_dir="./.logs/buysell",
)

c.run()
```


# Getting to Know The Platform

Making a system both flexible and easy to use is a hard task. We have thus decided to break
flexibility in some parts of the system to make it easier to implement new tasks. This is a choice, that 
is kind of bad under a point of view of system design but so there is only so much we can do.

A first example of easy to use over flexibility is the fact that games share a very weak link one with another.
This means that if you want to modify a game, you might as well copy-paste the entire game and modify it to your needs,
as opposed to inheriting some abstract class.


## Agents

The Agents we define are simple abstractions on top of Large Language Models. They are stateless 
for the most part, meaning that the only thing they are going to keep track of is the conversation history and some
minor variable to keep track of the game state. This is done to avoid having to deal with the complexity of 
giving agents access to the objects that represent the resources of the game.

Agents are called with predefined names that are available in the "constants" module.
Variables are `AGENT_ONE` and `AGENT_TWO` for the first and second agent respectively. 
Games rely on the fact that agents are named in this way to keep track of the conversation history.


