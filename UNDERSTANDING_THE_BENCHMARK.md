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