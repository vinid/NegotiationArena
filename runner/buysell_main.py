import sys
sys.path.append('.')
from dotenv import load_dotenv
import inspect
from game.agents.chatgpt import ChatGPTAgent
from game.agents.agent_behaviours import SelfCheckingAgent, ReasoningAgent
from game.game_objects.resource import Resources
from game.game_objects.goal import BuyerGoal, SellerGoal
from games.buyer_seller_game.buyer_seller_game import BuyerSellerGame

load_dotenv('.env')

class MyAgent(ChatGPTAgent, ReasoningAgent):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
  
    a1 = MyAgent(agent_name="Player 1", model="gpt-4-1106-preview")
    a2 = MyAgent(agent_name="Player 2", model="gpt-4-1106-preview")

    c = BuyerSellerGame(
            players=[a1,a2],
            iterations=6,
            resources_support_set = Resources({'X': 0, 'Y': 0}),
            player_goals = [SellerGoal(), BuyerGoal()],
            player_initial_resources = [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
            player_social_behaviour = ["",""],
            player_roles = ["You are Player 1, you are selling an object that you value at 60.", 
                            "You are Player 2, you are buying an object that you value at 40"]
        )
    
    c.run()
    