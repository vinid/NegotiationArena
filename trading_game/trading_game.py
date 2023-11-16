import sys
sys.path.append('.')
import os
import json
from game.logging import GameEncoder
from game.game import AlternatingGame, CommunicationGame
from game.constants import (
    MESSAGE_TAG,
    RESOURCES_TAG,
    GOALS_TAG,
    PLAYER_RESPONSE_TAG,
    PROPOSED_TRADE_TAG,
    REASONING_TAG,

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
                                                              PLAYER_RESPONSE_TAG, PROPOSED_TRADE_TAG, REASONING_TAG]
        ])
        self.parser.add_parse_rules([
            ResourcesParseRule(RESOURCES_TAG),
            GoalsParseRule(GOALS_TAG),
            ProposedTradeParseRule(PROPOSED_TRADE_TAG),
            UnformattedParseRule(PLAYER_RESPONSE_TAG),  
            UnformattedParseRule(REASONING_TAG),  
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

        self.game_settings = dict(
                resources_support_set=resources_support_set,
                player_goals=player_goals,
                player_initial_resources=player_initial_resources,
                player_social_behaviour=player_social_behaviour,
                player_roles=player_roles
        )
        self.game_state.append(
            {
                'iteration':'START',
                'turn': 'None',
                'settings': self.game_settings,
            }
        )

    def read_game_state(self, iteration):
        if iteration < 0:
            return {}
        else:
            return self.game_state[iteration]
        

    def write_game_state(self, players, response, iteration):
        # parse response
        
        parsed_response = self.parser.parse(response)
        datum = dict(iteration=iteration,
                     turn=self.turn,
                     response=parsed_response,
                     raw_response=response,
                     player_state=[player.get_state() for player in players])

        self.game_state.append(datum)
    
    def log_state(self):
        """
        Deplorable logging code
        
        log readable version of game state
        """
        super().log_state()
        settings = self.game_state[0]['settings']
        
        # log meta information
        log_str='Game Settings\n\n'
        for idx, player_settings in  enumerate(zip(*[[(k,str(p)) for p in v] for k,v in settings.items() if k!='resources_support_set'])):
            log_str+="Player {} Settings:\n".format(idx+1)
            log_str+='\n'.join(['\t{}: {}'.format(_[0], _[1]) for _ in player_settings])
            log_str+='\n\n'
        log_str+='------------------ \n'
            

        # log game state
        for state in self.game_state[1:-1]:
            turn = state['turn']
            data = [
                'Iteration: {}'.format(state['iteration']),
                'Turn: {}'.format(state['turn']),
                # 'Goals: {}'.format(settings['player_goals'][turn]),
                # 'Resources: {}'.format(settings['player_initial_resources'][turn]),
                *[ "{}: {}".format(k,v) for k,v in state['response'].items() if k!='raw_response']
            ]
            log_str += '\n'.join(data)
            log_str += '\n\n'

        # log game summary


        with open(os.path.join(self.log_path,'interaction.log'),'w') as f:
            f.write(log_str)

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

    def check_winner(self):
        print('CHECKING WINNER')
        end_state = self.game_state[-1]
        player_response = end_state['response'][PLAYER_RESPONSE_TAG]
        initial_resources = self.game_settings['player_initial_resources']
        player_goals = self.game_settings['player_goals']
        proposed_trade = self.game_state[-2]['response'][PROPOSED_TRADE_TAG]
        if player_response == 'ACCEPTED':
            # get proposed trade
            final_resources = [ proposed_trade.execute_trade(res, idx) for idx, res in enumerate(initial_resources)]
        else:
            final_resources = initial_resources
        
        outcome = [ goal.goal_reached(final) for goal,final in zip(player_goals, final_resources)]
        datum = dict(
            iteration='END',
            turn='None',
            player_goals=player_goals,
            initial_resources=initial_resources,
            proposed_trade=proposed_trade,
            final_response=player_response, # ACCEPT / REJECT / WAIT
            final_resources=final_resources,
            player_outcome=outcome,
        )
        
        self.game_state.append(datum)

    def kill_players(self):
        # do nothing
        return

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
    from game.agents.agents import SelfCheckingAgent
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

    class SelfCheckingGPT(ChatGPTAgent, SelfCheckingAgent):
        def __init__(self,**kwargs):
            super().__init__(**kwargs)


    a1 = ChatGPTAgent(agent_name="Player 1", model="gpt-4-1106-preview")
    a2 = SelfCheckingGPT(agent_name="Player 2", model="gpt-4-1106-preview")

    c = TradingCommGame(
            players=[a1,a2],
            iterations=5,
            resources_support_set = Resources({'X': 0, 'Y': 0}),
            player_goals = [ResourceGoal({"X": 15, "Y": 16}), ResourceGoal({"X": 15, "Y": 15})],
            player_initial_resources = [Resources({"X": 25, "Y": 5}), Resources({"X": 5, "Y": 25})],
            player_social_behaviour = ["",""],
            player_roles = ["You are Player 1, start by making a proposal.", "You are Player 2, start by responding to a trade."]
        )
    
    c.run()