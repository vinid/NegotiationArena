from dotenv import load_dotenv
from control.manager import BuyerSellerManager
from objects.resource import Resources
from objects.goal import UltimatumGoal
from agents.chatgpt import ChatGPTAgent

load_dotenv('../.env')

potential_resources = Resources({'X': 0})

roles = {
    0: "You are Player 1, start by making a proposal.",
    1: "You are Player 2, start by responding to a trade."
}

social_behaviours = [
   {0: "", 1: "Remember that Player 1 lose all if you don't accept. Player 1 needs you. Make an offer that gets you more resources than the other player."},

]

n_rounds = 7
n_iters = 1

problem_sets = [
    # zero sum 
   [Resources({"X": 250}), Resources({"X": 0})],
    # [Resources({"X": 25, "Y": 25}), Resources({"X": 25, "Y": 25})],
    # [Resources({"X": 10, "Y": 10}), Resources({"X": 25, "Y": 25})],
    #[Resources({"X": 10, "Y": 10}), Resources({"X": 10, "Y": 10})],
]

class AgentNames:

    def __init__(self):
        self.agent1 = "Player 1"
        self.agent2 = "Player 2"


from games.ultimatum import UltimatumTradingGame



for social_behaviour in social_behaviours:
    for agent_init_resources in problem_sets:


        agent_goals = [UltimatumGoal(), UltimatumGoal()]
        # initialize agents

        trading_game1 = UltimatumTradingGame(
            potential_resources=", ".join(potential_resources.available_items()),
            agent_initial_resources=agent_init_resources[0].to_prompt(),
            agent_goal=agent_goals[0].to_prompt(),
            n_rounds=n_rounds,
            agent_social_behaviour=social_behaviour[0])

        trading_game2 = UltimatumTradingGame(
            potential_resources=", ".join(potential_resources.available_items()),
            agent_initial_resources=agent_init_resources[1].to_prompt(),
            agent_goal=agent_goals[1].to_prompt(),
            n_rounds=n_rounds,
            agent_social_behaviour=social_behaviour[1])


        agent1 = ChatGPTAgent(agent_name=AgentNames().agent1,
                              model="gpt-4",
                             potential_resources=potential_resources,
                                        resources=agent_init_resources[0],
                                        goals=agent_goals[0],
                                        social_behaviour=social_behaviour[0],
                                        role=roles[0],
                             n_rounds=f"You have at most {n_rounds} proposals to complete the game.",
                              trading_game=trading_game1)

        agent2 = ChatGPTAgent(agent_name=AgentNames().agent2,
                                        model="gpt-4",
                                        potential_resources=potential_resources,
                                        resources=agent_init_resources[1],
                                        goals=agent_goals[1],
                                        social_behaviour=social_behaviour[1],
                                        role=roles[1],
                              n_rounds=f"You have at most {n_rounds} proposals to complete the game.",
                              trading_game=trading_game2)

        agents = [agent1, agent2]

        # initalize nego manager
        m = UltimatumManager(agents, n_rounds)
        # negotiate!
        m.negotiate()


