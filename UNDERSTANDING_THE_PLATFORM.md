# Understanding the Benchmark

## Roles

Roles in LLMs identify the turns. We assume that most of the times, the setting is as follows:

```
System Prompt
User Message
Assistant Message
User Message
Assistant Message
...
```
This makes a bit complex to define how to agents should chat. We 
do this with roles. The first agent acts first and thus, this agent is going to
be prompted by a user message.

```
(First Agent)
System Prompt: *Description of the Game*
User Message: You are Player 1, Make an Offer
...
```
This problem does not exist for the second player as it is going to reply to a "user message" that will
be Player 1 message.

```
(Second Agent)
System Prompt: *Description of the Game* You are Player 2. 
...
```

# State


## Manager

The manager is the main object that runs the entire game


## Game


## Agents

The Agents we define are simple abstractions on top of Large Language Models. They are stateless 
for the most part, meaning that the only thing they are going to keep track of is the conversation history and some
minor variable to keep track of the game state. This is done to avoid having to deal with the complexity of 
giving agents access to the objects that represent the resources of the game.

Agents are called with predefined names that are available in the "constants" module.
Variables are `AGENT_ONE` and `AGENT_TWO` for the first and second agent respectively. 
Games rely on the fact that agents are named in this way to keep track of the conversation history.

### Known Issues
