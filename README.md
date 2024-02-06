# How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z1M97k4GEf2_v48cdA96BANTAp0yK2IM?usp=sharing)
[![Arxiv Preprint](https://img.shields.io/badge/arXiv-xxx.xxx-xxx.svg)](https://arxiv.org/abs/12.xxxx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<p align="center">
<img src="figures/negotiation_intro.jpg" width="400"/>
</p>

## Abstract

Negotiation is the basis of social interactions; humans negotiate everything from the price of cars to how to share common resources. With rapidly growing interest in using large language models (LLMs) to act as agents on behalf of human users, such LLM agents would also need to be able to negotiate. In this paper, we study how well LLMs can negotiate with each other. We develop NegotiationArena: a flexible framework for evaluating and probing the negotiation abilities of LLM agents.

## Quick Tutorial

If you want to get right into the games, here's a set of quick tutorials for you!

| Task                                | Link     |
|-------------------------------------|----------|
| 1 - Running Buy and Sell Scenario   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z1M97k4GEf2_v48cdA96BANTAp0yK2IM?usp=sharing)|
| 2 - Exploring Buy and Sell Results  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z1M97k4GEf2_v48cdA96BANTAp0yK2IM?usp=sharing)|
| 3 - Building a Scenario From Scrach | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z1M97k4GEf2_v48cdA96BANTAp0yK2IM?usp=sharing)|


## What Can This Platform Be Used For

### Running Evals on Agents

### Reasoning and Social Behavior
Explore reasoning and social behavior of LLMs. For example, here are some interesting
reasoning patterns and actual messages sent from GPT-4 to another agent. In image 2 and 3 
GPT-4 was initialized to have a specific behavior.

<p align="center">
<img src="figures/gpt_4_interesting_messages.png" width="500">
</p>

### Understanding New Patterns in LLMs

### Building New Games

## News: Refactroing

We are currently refactoring some of the scenarios. If you want the complete scenarios 
you can access the Paper Experiment Branch [here](https://github.com/vinid/NegotiationArena/tree/paper_experiment_code).

| Task                       | Status   |
|----------------------------|----------|
| Buy Sell Scenario          | Done     |
| Resource Exchange Scenario | Not Done |
| Ultimatum Scenario         | Done     |



## Quick How To: Running One of the Scenarios

Running and modifying a game is relatively easy. 

First step. Agents requires API keys to be set in the environment variables. You can do this in a .env file.
    
```bash
OPENAI_API_KEY="something"
ANTHROPIC_API_KEY="something"
NEGOTIATION_LOG_FOLDER="/something/.logs/"
ANY_SCALE="something"
```
ANY_SCALE is optional. It is used to run LLaMA in case you want to try that.


### Instantiate Agents

Agents only keep track of the conversation they are doing. Agents object cannot and should
not be reused. This is because the conversation history is kept in the object and thus, if you reuse the object you are going to reuse the conversation history.

```python
a1 = ChatGPTAgent(agent_name="Player 1", model="gpt-4-1106-preview")
a2 = ChatGPTAgent(agent_name="Player 2", model="gpt-4-1106-preview")
```
### Instantiate the Game

```python

c = BuySellGame(players=[a1, a2],
    iterations=10,
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
        "",  
    ],
    log_dir="./.logs/buysell",
)
```

```python
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




