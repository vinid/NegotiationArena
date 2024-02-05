# How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z1M97k4GEf2_v48cdA96BANTAp0yK2IM?usp=sharing)


![image](figures/negotiation_intro.jpg)

Negotiation is the basis of social interactions; humans negotiate everything from the price of cars to how to share common resources. With rapidly growing interest in using large language models (LLMs) to act as agents on behalf of human users, such LLM agents would also need to be able to negotiate. In this paper, we study how well LLMs can negotiate with each other. We develop NegotiationArena: a flexible framework for evaluating and probing the negotiation abilities of LLM agents. We implemented three types of scenarios in \name~to assess LLM's behaviors in allocating shared resources (ultimatum games), aggregate resources (trading games) and buy/sell goods (price negotiations).  

## Quick How To



Running and modifying a game is relatively easy

Agents requires API keys to be set in the environment variables. You can do this in a .env file.
    
```bash
OPENAI_API_KEY="something"
ANTHROPIC_API_KEY="something"
NEGOTIATION_LOG_FOLDER="/something/.logs/"
ANY_SCALE="something"
```

```python
a1 = ChatGPTAgent(agent_name="Player 1", model="gpt-4-1106-preview")
a2 = ChatGPTAgent(agent_name="Player 2", model="gpt-4-1106-preview")

c = BuySellGame(players=[a1, a2],
    game_interface=BuySellGameInterface(),
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

We are happy for any suggestion you might have on how to improve the system. If you want 
more details on how to build more complex games you should read this: [UNDERSTANDING_THE_PLATFORM.md](UNDERSTANDING_THE_PLATFORM.md).




