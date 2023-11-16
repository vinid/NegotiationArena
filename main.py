from dotenv import load_dotenv
from game.agents.chatgpt import ChatGPTAgent
from game.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import ResourceGoal
from trading_game.trading_game import TradingGame

load_dotenv('.env')


class MyAgent(ChatGPTAgent, SelfCheckingAgent, ReasoningAgent):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

if __name__ == "__main__":
  
    a1 = MyAgent(agent_name="Player 1", model="gpt-4-1106-preview")
    a2 = MyAgent(agent_name="Player 2", model="gpt-4-1106-preview")

    c = TradingGame(
            players=[a1,a2],
            iterations=5,
            resources_support_set = Resources({'X': 0, 'Y': 0}),
            player_goals = [ResourceGoal({"X": 15, "Y": 16}), ResourceGoal({"X": 15, "Y": 15})],
            player_initial_resources = [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
            player_social_behaviour = ["",""],
            player_roles = ["You are Player 1, start by making a proposal.", "You are Player 2, start by responding to a trade."]
        )
    
    c.run()