import os
import time
from pathlib import Path
from agents import *
from typing import List
from utils import *
import logging
from prompts import *
from log_dumper import LogDumper
from collections import defaultdict, OrderedDict
from utils import StateTracker

LOGGING_PATH = os.environ.get("NEGOTIATION_LOG_FOLDER", ".logs")

class Manager:

    def __init__(self, 
                 agents: List[ChatGPTAgent], 
                 n_rounds, 
                 model="gpt-4",
                 log: bool = True
    ):  
        self.agents = agents
        # initialize agent with empty state
        self.agents_state = [[StateTracker()] for _ in self.agents]
        self.n_rounds = n_rounds
        self.model = model
        self.message_queue = []
        self.message_history = []
        
        # start with agent 0
        self.turn = 0
        
        # initialize agents with init_prompt
        for agent in self.agents:
            agent.init_agent()
            

        # logging init 
        run_epoch_time_ms = round(time.time() * 1000)               
        
        # create datastore path
        self.log_path = os.path.join(LOGGING_PATH,str(run_epoch_time_ms))
        self.log_dumper = LogDumper(self.log_path)

        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            format='%(message)s',
            level=logging.INFO,
            filename=os.path.join(self.log_path,'interaction.log'),
            force=True
        )

        
    def negotiate(self):
        pm = PromptManager()

        # negotiation over rounds
        for iteration in range(0, self.n_rounds*2):
            state_tracker = StateTracker()
            print("Iteration: {}".format(iteration))
            
            logging.info("Iteration: {}".format(iteration))
            logging.info("Turn: Player {}\n".format(self.turn))
            
            # if there are messages in queue
            if self.message_queue:
                # extract messages from queue
                # assume for now only one message
                self.agent[self.turn].receive_messages(self.message_queue.pop())

            # update beliefs upon new message
            self.agent[self.turn].update_beliefs()

            # make agent think about and make a trade
            self.agent[self.turn].make_trade()
                        
            # update agent state
            # self.agents_state[self.turn].append({"player_response": trade_decision, "proposed_trade": trade_proposal})
            self.agents_state[self.turn].append(state_tracker)

            # structured_state["iter"] = i
            


            # debug
            # print("\nPlayer State: {}".format(structured_state))
            # for k,v in self.agents_state[self.turn].items():
            #     print(k,":",v)
            # print('=====\n')
            logging.info("\nPlayer State: {}".format(state_tracker))
            for k,v in self.agents_state[self.turn][-1].__dict__.items():
                logging.info("{}:{}".format(k,v))
            logging.info('=====\n')
            
            print(state_tracker.player_response)
            end = self.check_exit_condition(state_tracker.player_response, i)

            if end:
                return end
            
            # logic to update agent turn
            self.turn = 0 if self.turn == 1 else 1

        return "GAMEOVER"

    def check_exit_condition(self, decision, iter):
        """
        Extract agent beliefs at the end negotiation and check of goal is met
        """

        agents_final_resources, agents_initial_resources = [], []
        init_res_sum, final_res_sum = None, None

        logging.info(('\n\n'))
        # IF ACCEPTED OR LAST ITERATION
        if decision == "ACCEPTED" or iter == (self.n_rounds*2 - 1):
            for idx, agent in enumerate(self.agents):
                # request beliefs
                agent.update_conversation_tracking("system", asking_for_final_results.format(decision))
                response = agent.chat()
                # update conversation tracker
                agent.update_conversation_tracking("assistant", response)

                response_lines = [ _ for _ in response.splitlines() if _.strip('\n')]

                final_resources = response_lines[2].split("FINAL RESOURCES: ")[1]
                final_resources = Resources(text_to_dict(final_resources))

                agents_final_resources.append(final_resources)
                agents_initial_resources.append(agent.inital_resources)

                logging.info("R{} INITIAL : {}".format(idx, str(agent.inital_resources)))
                logging.info("R{} FINAL   : {}".format(idx, str(final_resources)))
                logging.info("R{} GOAL    : {}\n".format(idx, str(agent.goals)))

                init_res_sum = agent.inital_resources if init_res_sum is None else init_res_sum + agent.inital_resources
                final_res_sum = final_resources if final_res_sum is None else final_res_sum + final_resources

            # check resources remain consistent at start and end of negotiation
            if not final_res_sum.equal(init_res_sum):
                logging.info("The sum of the resources is not the same as the original sum!")
                logging.info("Original sum:", init_res_sum)
                logging.info("Final sum:", final_res_sum)

            results_of_negotiation = []
            for idx, agent_res in enumerate(agents_final_resources):
                if self.agents[idx].goals.goal_reached(agent_res):
                    logging.info("Agent {} REACHED the goal!".format(idx))
                    results_of_negotiation.append(True)
                else:
                    logging.info("Agent {} DID NOT reach the goal!".format(idx))
                    results_of_negotiation.append(False)
            logging.info("\n\n")

            self.log_dumper.dump_conversation(self.agents)
            self.log_dumper.dump_agent_state(self.agents_state)

            # some run stats
            scores = []
            for v1, v2 in zip(agents_final_resources, agents_initial_resources):
                s = v1 - v2
                scores.append(s.value())
        
            return {
                "resources_consistent": final_res_sum.equal(init_res_sum),
                "negotiation_result": results_of_negotiation,
                "scores": scores,
                "end_iter": iter
            }

        else:
            return False

    def __exit__(self):
        for idx, agent in enumerate(self.agents):
            agent.dump_conversation(os.path.join(self.log_path,"agent_{}.txt".format(idx)))

    def log(self):
        """
        Log conversation in human interpretable format
        """


class PromptManager:

    def __init__(self):
        pass

    def trade_formatter(self, opponent_proposal, opponent_decision):

        opponent_response = None

        # append opponent response from previous iteration
        if opponent_proposal or opponent_decision:
            if opponent_decision:
                opponent_response = "PLAYER RESPONSE : {}".format(opponent_decision) + "\n" + \
                                    "NEWLY PROPOSED TRADE : {}".format(opponent_proposal.to_prompt())
            else:
                opponent_response = "NEWLY PROPOSED TRADE : {}".format(opponent_proposal.to_prompt())

        return opponent_response
