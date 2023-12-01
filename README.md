# Getting to Know The Platform

Making a system both flexible and easy to use is a hard task. We have thus decided to break
flexibility in some parts of the system to make it easier to implement new tasks.



## Manager

The manager is the main object that runs the entire game


## Game


## Agents

The Agents we define are simple abstractions on top of Large Language Models. They are stateless 
for the most part, meaning that the only thing they are going to keep track of is the conversation history and some
minor variable to keep track of the game state. This is done to avoid having to deal with the complexity of 
giving agents access to the objects that represent the resources of the game.


### Unstable Components

Games rely on the fact that agetns are named "Player 1" and "Player 2", changing them can break the game.

### Game

