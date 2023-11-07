import os
import time
from pathlib import Path
from typing import List
import logging
from control.logging_support import LogDumpHandler
from objects.utils import StateTracker
from agents.agents import Agent
from objects.goal import ResourceGoal, MaximisationGoal
from objects.utils import parse_response
from objects.message import Message

class Manager:

    def __init__(self,
                 agents: List[Agent],
                 n_rounds,
                 additional_game_metadata=None
                 ):
        self.agents = agents
        # initialize agent with empty state
        self.tracking_states = dict()

        self.tracking_states["states"] = [[StateTracker(iteration=-1,
                                                        goals=agent.goals,
                                                        resources=agent.resources[0])] for agent in self.agents]

        self.n_rounds = n_rounds
        self.global_message_queue = []
        self.message_history = [] # TODO: what is this?

        logging_path = os.environ.get("NEGOTIATION_LOG_FOLDER")
        # start with agent 0
        self.turn = 0
        
        # initialize agents with init_prompt
        for agent in self.agents:
            agent.init_agent()

        # logging init 
        run_epoch_time_ms = round(time.time() * 1000)               
        print(logging_path)
        # create datastore path
        self.log_path = os.path.join(logging_path,str(run_epoch_time_ms))
        self.log_dumper = LogDumpHandler(self.log_path)

        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        self.tracking_states["metadata"] = {
            "n_rounds": self.n_rounds,
            "agents": [agent.model for agent in self.agents],
            "starting_resources": [str(agent.resources[0]) for agent in self.agents],
            "goals": [str(agent.goals) for agent in self.agents],
            "additional_metadata": additional_game_metadata}

        logging.basicConfig(
            format='%(message)s',
            level=logging.INFO,
            filename=os.path.join(self.log_path,' interaction.log'),
            force=True
        )

        
    def negotiate(self):

        # negotiation over rounds
        # even rounds will be player 1 talking
        # odd rounds will be player 2 talking
        # patrick said it was a good idea to do it this way

        for iteration in range(0, self.n_rounds*2):

            # state tracker keeps track of state of the game
            state_tracker = StateTracker()
            state_tracker.iteration = iteration
            state_tracker.goals = self.agents[self.turn].goals
            state_tracker.set_resources(self.agents[self.turn].resources[-1])
            state_tracker.set_agent_in_turn(self.agents[self.turn].model)

            print("Iteration: {}".format(iteration))
            logging.info("Iteration: {}".format(iteration))
            logging.info("Turn: Player {}\n".format(self.turn))
            
            # if there are messages in queue
            if self.global_message_queue:
                # extract messages from queue
                # assume for now only one message
                received_msg = self.global_message_queue.pop()
                self.message_history.append(received_msg)
                self.agents[self.turn].receive_messages(received_msg)
                # update state tracker
                state_tracker.set_player_response(received_msg.data['player_response'])
                state_tracker.set_received_trade(received_msg.data['proposed_trade'])
                state_tracker.set_received_message(received_msg.data['message'])

            # # update beliefs (usually if there is new message)
            # self.agents[self.turn].update_beliefs()

            # make agent think about and make a trade
            response = self.agents[self.turn].think_next_action()

            # parse the response
            my_resources, player_response, proposed_trade, message, player_reason = parse_response(response)
            state_tracker.set_reasoning(player_reason)

            # send a message
            message = Message({
                "proposed_trade": proposed_trade,
                "player_response": player_response,
                "message": message
            })

            self.global_message_queue.append(message)

            # update state tracker
            state_tracker.setattrs(**message.data)

            # iteration is over, we update global agent states with the state tracker
            self.tracking_states["states"][self.turn].append(state_tracker)

            # logging
            logging.info("\nPlayer State: {}".format(state_tracker))
            for k,v in self.tracking_states["states"][self.turn][-1].__dict__.items():
                logging.info("{}:{}".format(k,str(v)))
            logging.info('=====\n')
        
            end = self.check_exit_condition(state_tracker.player_response, state_tracker.received_trade, iteration)

            if end:
                return end
    
            # logic to update agent turn
            self.turn = 1 - self.turn

    def check_exit_condition(self, decision, trade, iteration):
        """
        Extract agent beliefs at the end negotiation and check of goal is met
        """
        # IF ACCEPTED OR LAST ITERATION
        if decision == "ACCEPTED" or iteration == (self.n_rounds*2 - 1):
            for idx, agent in enumerate(self.agents):
                # kill agent
                agent.kill(decision)
                
                state_tracker = StateTracker()
                state_tracker.iteration = iteration + 1
                state_tracker.goals = agent.goals
                # get end state resources
                #actual_final_resources = trade.execute_trade(agent.resources[-2], idx) if decision=='ACCEPTED' else agent.resources[-2]
                
                state_tracker.resources = agent.resources[-1]
                state_tracker.player_response = decision
                self.tracking_states["states"][idx].append(state_tracker)

                # THIS IS BASED ON AGENT INTERAL BELIEFS
                if isinstance(agent.goals, ResourceGoal):
                    if agent.goals.goal_reached(agent.resources[-1]):
                        logging.info("Agent {} thinks it REACHED the goal!".format(idx))
                    else:
                        logging.info("Agent {} thinks it DID NOT reach the goal!".format(idx))
                elif isinstance(agent.goals, MaximisationGoal):
                    resource_gain = agent.goals.goal_reached(agent.resources[0], agent.resources[-1])
                    logging.info("Agent {} has obtained resources {}".format(idx, resource_gain))
                    
                
                # if agent.goals.goal_reached(actual_final_resources):
                #     logging.info("Agent {} REACHED the goal!\n".format(idx))
                # else:
                #     logging.info("Agent {} DID NOT reach the goal!\n".format(idx))
                #
            self.log_dumper.dump_conversation(self.agents)
            self.log_dumper.dump_agent_state(self.tracking_states)

            return True
        
        return False

    def __exit__(self):
        for idx, agent in enumerate(self.agents):
            agent.dump_conversation(os.path.join(self.log_path,"agent_{}.txt".format(idx)))

    def log(self):
        """
        Log conversation in human interpretable format
        """


