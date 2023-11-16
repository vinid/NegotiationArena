import sys
sys.path.append('.')
from game.game import AlternatingGame, CommunicationGame
from game.constants import (
    MESSAGE_TAG,
    RESOURCES_TAG,
    GOALS_TAG,
    PLAYER_RESPONSE_TAG,
    PROPOSED_TRADE_TAG
)
from game.parser import Parser, UnformattedParseRule
from trading_parser import ResourcesParseRule, GoalsParseRule, ProposedTradeParseRule
from trading_prompts import NegotiationPrompt
from game.prompt_builder import Prompt

class TradingGame(AlternatingGame):
    
    def __init__(self, 
                 resources_support_set,
                 player_goals,
                 player_initial_resources,
                 player_social_behaviour,
                 player_roles,
                 **kwargs
    ):
        super().__init__(**kwargs)
        self.response_format_prompt.append([
            "<{0}> [add here] </{0}>".format(tag) for tag in [RESOURCES_TAG, GOALS_TAG,
                                                              PLAYER_RESPONSE_TAG, PROPOSED_TRADE_TAG]
        ])
        self.parser.add_parse_rules([
            ResourcesParseRule(RESOURCES_TAG),
            GoalsParseRule(GOALS_TAG),
            ProposedTradeParseRule(PROPOSED_TRADE_TAG),
            UnformattedParseRule(PLAYER_RESPONSE_TAG),  
        ])
        self.base_prompt = NegotiationPrompt
        
        # TODO: HOT FIX
        format_pre = Prompt([
            "All the responses you send should contain the following and in this order.\n",
            "```",
        ])
        format_post = Prompt([
            "```",
            "Please be sure to include all.\n",
        ])
    
        # initialize players
        for idx, player in enumerate(self.players):
            game_prompt = NegotiationPrompt(
                resources_support_set,
                agent_initial_resources=player_initial_resources[idx],
                agent_goal=player_goals[idx],
                n_rounds = self.iterations//2,
                agent_social_behaviour=player_social_behaviour[idx]
            )
            
            player.init_agent(game_prompt+format_pre+self.response_format_prompt+format_post+Prompt([player_roles[idx]]))

    def read_game_state(self, iteration):
        if iteration < 0:
            return {}
        else:
            return self.game_state[iteration]
        

    def write_game_state(self, player, response, iteration):
        # parse response
        
        parsed_response = self.parser.parse(response)
        datum = dict(iteration=iteration,
                     turn=self.turn,
                     response=parsed_response,
                     raw_response=response,
                     player_state=player.get_state())

        self.game_state.append(datum)
        

    def game_over(self):
        """
        game over logic based on game state
        """
        state = self.game_state[-1]

        if state:
            response = state['response'].get(PLAYER_RESPONSE_TAG, 'WAIT')
            iteration = state.get('iteration', 0)
            if response == 'ACCEPTED' or iteration == self.iterations:
                return True
        return False

    def get_next_player(self):
        """
        player turn semantics
        """
        self.turn = 1-self.turn

# CommunicationGame
class TradingCommGame(TradingGame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    

if __name__ == "__main__":
    from dotenv import load_dotenv
    from game.agents.chatgpt import ChatGPTAgent
    from game.game_objects.resource import Resources
    from game.game_objects.goal import ResourceGoal
    load_dotenv('.env')
    
    potential_resources = Resources({'X': 0, 'Y': 0})
    agent_goals = [ResourceGoal({"X": 15, "Y": 16}), ResourceGoal({"X": 10, "Y": 15})]
    agent_resources = [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})]
    social_behaviour = ["",""]
    roles = {
        0: "You are Player 1, start by making a proposal.",
        1: "You are Player 2, start by responding to a trade."
    }

    a1 = ChatGPTAgent(agent_name="Player 1", model="gpt-3.5-turbo")
                    
    a2 = ChatGPTAgent(agent_name="Player 1", model="gpt-4-1106-preview")

    c = TradingCommGame(
            players=[a1,a2],
            iterations=5,
            resources_support_set = Resources({'X': 0, 'Y': 0}),
            player_goals = [ResourceGoal({"X": 15, "Y": 15}), ResourceGoal({"X": 10, "Y": 15})],
            player_initial_resources = [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
            player_social_behaviour = ["",""],
            player_roles = ["You are Player 1, start by making a proposal.", "You are Player 2, start by responding to a trade."]
        )
    
    c.run()