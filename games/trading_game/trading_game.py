import sys
sys.path.append('.')
import os
from game.logging import GameEncoder
from game.game import AlternatingGame, CommunicationGame
from game.constants import (
    RESOURCES_TAG,
    GOALS_TAG,
    PLAYER_RESPONSE_TAG,
    PROPOSED_TRADE_TAG,
)
from game.parser import UnformattedParseRule,  PassThroughParseRule
from games.trading_game.trading_parser import ResourcesParseRule, GoalsParseRule, ProposedTradeParseRule
from games.trading_game.trading_prompts import NegotiationPrompt
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
          # Initialze game state
        self.game_state =[{
            'iteration':'START',
            'turn': 'None',
            'settings': dict(
                    resources_support_set=resources_support_set,
                    player_goals=player_goals,
                    player_initial_resources=player_initial_resources,
                    player_social_behaviour=player_social_behaviour,
                    player_roles=player_roles)
        }]
        self.init_parser()
        # init players
        self.init_players()

    def init_parser(self):
        self.global_parser.add_parse_rules([
            ResourcesParseRule(RESOURCES_TAG),
            GoalsParseRule(GOALS_TAG),
            UnformattedParseRule(PLAYER_RESPONSE_TAG),  
            ProposedTradeParseRule(PROPOSED_TRADE_TAG),
        ])
        self.public_parser.add_parse_rules([
            PassThroughParseRule(PLAYER_RESPONSE_TAG), 
            PassThroughParseRule(PROPOSED_TRADE_TAG),
        ])

    def init_players(self):
        for idx, player in enumerate(self.players):
            game_prompt = self.game_prompt(
                self.game_state[0]['settings']['resources_support_set'],
                agent_initial_resources=self.game_state[0]['settings']['player_initial_resources'][idx],
                agent_goal=self.game_state[0]['settings']['player_goals'][idx],
                n_rounds = self.iterations//2- 1 ,
                agent_social_behaviour=self.game_state[0]['settings']['player_social_behaviour'][idx]
            )
            player.init_agent(game_prompt+\
                              self.global_parser.get_response_format_prompt()+\
                              Prompt([self.game_state[0]['settings']['player_roles'][idx]]))
            

    @property
    def game_prompt(self):
        return NegotiationPrompt

    def read_game_state(self, iteration):
        datumn = self.game_state[iteration].get('player_response', None)
        datumn = {} if datumn is None else {'player_response':  datumn}
        return datumn
        
    def write_game_state(self, players, response, iteration):
        # parse response
        parsed_response = self.global_parser.parse(response)
        # parse for sharing between players
        parsed_public_response = self.public_parser.parse(response)
        parsed_public_response = "```\n"  + "\n".join(parsed_public_response.values()) + "\n```"
        datum = dict(iteration=iteration,
                     turn=self.turn,
                     response=parsed_response,
                     raw_response=response,
                     player_response=parsed_public_response,
                     player_state=[player.get_state() for player in players])

        self.game_state.append(datum)
    
    def get_next_player(self):
        """
        player turn logic
        """
        self.turn = 1-self.turn

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
        end_state = self.game_state[-1]
        player_response = end_state['response'][PLAYER_RESPONSE_TAG]
        initial_resources = self.game_state[0]['settings']['player_initial_resources']
        player_goals = self.game_state[0]['settings']['player_goals']
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
            summary=dict(
                player_goals=player_goals,
                initial_resources=initial_resources,
                proposed_trade=proposed_trade,
                final_response=player_response, # ACCEPT / REJECT / WAIT
                final_resources=final_resources,
                player_outcome=outcome
            )
        )
        
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
        for state in self.game_state[1:]:
            # turn = state['turn']
            if state['iteration'] == "END":
                continue 
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
        log_str+='------------------ \n'
        if self.game_state[-1]['iteration'] == "END":
            state = self.game_state[-1]
            data = [
                    'Iteration: {}'.format(state['iteration']),
                    'Turn: {}'.format(state['turn']),
                    *[ "{}: {}".format(k,v) for k,v in state['summary'].items()]
            ]
            log_str += '\n'.join(data)

        # write to log-file
        with open(os.path.join(self.log_path,'interaction.log'),'w') as f:
            f.write(log_str)


# CommunicationGame
class TradingCommGame(CommunicationGame, TradingGame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.init_players()
