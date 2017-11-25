from strategy import *
from blackjack import * 

def fitness_score(strat,num_trials):
	score=0
	for i in range(0,num_trials):
		score += play_one_game(strat)
	return score

s = generate_strategy()
print fitness_score(s,1000)
