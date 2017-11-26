from strategy import *
from blackjack import *

def fitness_scores(strat,num_trials):
	scores = []
	for i in range(0,num_trials):
		scores.append(play_one_game(strat))
	return scores

#s = generate_strategy()
#print fitness_score(s,1000)
