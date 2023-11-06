import os
import json
class LogDumper:

    def __init__(self, log_path):
        self.log_path = log_path

    def dump_conversation(self, agents):

        for idx, agent in enumerate(agents):
            agent.dump_conversation(os.path.join(self.log_path, "agent_{}.txt".format(idx)))

    def dump_agent_state(self, state):
        """
        Dump agent state into log
        """

        # dump state info into log
        with open(os.path.join(self.log_path, 'state.json'), 'w') as f:
            metadata = state["metadata"]
            tracking = state["states"]

            tr = [[{k: str(v) for k, v in s.__dict__.items()} for s in st] for st in tracking]

            dumped = {"metadata": metadata, "states": tr}

            json.dump(dumped, f, indent=4)