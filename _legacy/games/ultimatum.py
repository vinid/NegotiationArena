import logging
from objects.resource import Resources
from objects.trade import Trade
from objects.utils import RuleBook
from objects.utils import Parser, text_to_dict
from games.ultimatum_prompts import *


def get_rulebook():
    return UltimatumRuleBook(ParserUltimatum())

## Number of rounds
class RoundsPrompt(Prompt):
    def __init__(self, n_rounds: int):
        self.prompts = [
           "\nYou have at most {} proposals to complete the game.".format(n_rounds)
        ]

        super().__init__(
           [str(p) for p in self.prompts]
        )


# Overall Prompt
class UltimatumRuleBook(RuleBook):

    def __init__(self, parser):
        super().__init__(parser)

    def instantiate_initial_prompt(self, potential_resources,
                                   agent_initial_resources,
                                   agent_goal,
                                   n_rounds,
                                   agent_social_behaviour):
        return UltimatumPrompt(
            potential_resources=potential_resources,
            agent_initial_resources=agent_initial_resources,
            agent_goal=agent_goal,
            n_rounds=n_rounds,
            agent_social_behaviour=agent_social_behaviour)


class ParserUltimatum(Parser):

    def parse_response(self, response):

        start_index, end_index, tag_len = self.get_index_for_tag(RESOURCES_TAG, response)
        k = response[start_index + tag_len:end_index].strip()

        my_resources = Resources(text_to_dict(k))

        start_index, end_index, tag_len = self.get_index_for_tag(PROPOSED_TRADE_TAG, response)
        trade = response[start_index + tag_len:end_index].strip()

        if trade == "WAIT":
            proposed_trade = "WAIT"
        else:
            try:
                proposed_trade = Trade(self.parse_proposed_trade(trade), raw_string=trade)
            except:
                logging.error(f"Error parsing trade: {trade}")
                raise Exception

        start_index, end_index, tag_len = self.get_index_for_tag(MESSAGE_TAG, response)
        message = response[start_index + tag_len:end_index].strip()

        start_index, end_index, tag_len = self.get_index_for_tag(PLAYER_RESPONSE_TAG, response)
        player_response = response[start_index + tag_len:end_index].strip()

        start_index, end_index, tag_len = self.get_index_for_tag(REASONING_TAG, response)
        player_reason = response[start_index + tag_len:end_index].strip()

        return my_resources, player_response, proposed_trade, message, player_reason

    def parse_proposed_trade(self, s):
        trade = {}
        items = s.split(" Gets")
        for i in range(1, len(items)):
            item = items[i]
            prev_item = items[i - 1]
            player_id = str(prev_item[-2:].strip())
            subitem = item.split(" Player")[0].strip()
            try:
                resources = {k: float(v.replace(",", "").rstrip(".,;")) for k, v in
                             (item.split(": ") for item in subitem.split(", "))}
            except Exception as e:
                print(subitem)
                raise e

            trade[player_id] = resources
        return trade

    def prompt_for_final_results(self, decision):
        decision = decision.lower()

        asking_for_final_results = f"""The proposal was {decision}. The game is over. I am the game master. Tell me the following:

                  <{RESOURCES_TAG}> (these are your original resources) </{RESOURCES_TAG}>
                  <{decision} trade> (this is the trade that was {decision}) </{decision} trade>
                  <{FINAL_RESOURCES_TAG}> (this is what you have after this trade) </{FINAL_RESOURCES_TAG}> 
                  follow this formatting, do not add newlines where not needed.
                  """

        return asking_for_final_results

    def parse_final_resources(self, response):
        start_index, end_index, tag_len = self.get_index_for_tag(FINAL_RESOURCES_TAG, response)
        final_resources = response[start_index + tag_len:end_index].strip()
        return final_resources


class UltimatumPrompt(Prompt):

    def __init__(self,
                 potential_resources,
                 agent_initial_resources,
                 agent_goal,
                 n_rounds,
                 agent_social_behaviour):
        self.prompts = [
            intro,
            rules,
            AgentContextPrompt(potential_resources, agent_initial_resources, agent_goal),
            response_format,
            RoundsPrompt(n_rounds),
            Prompt(['', agent_social_behaviour]),
            agent_objective
        ]

        super().__init__(
            [str(self.prompts[i]) for i in range(len(self.prompts))]
        )

agent_objective = Prompt([
    "Your goal is to find a way to split the resources with the other player. If you do not find a way to reach an agreement on how to split the resources. You both lose all the resources.",
])




