from strategy import *
from blackjack import *

#Returns the fitness score of a given strategy and how many games should be played to
#determine the fitness_score. The fitness score is linear to net score.
def fitness_score_linear(strat,num_trials,alpha):
	score=0
	for i in range(0,num_trials):
		score += play_one_game(strat)
	#Fitness scores should be positive, so normalize to a minimum of 0.
	return min(0,alpha*score+2*num_trials)

#Returns the fitness score of a given strategy and how many games should be played to
#determine the fitness_score. The fitness score is a square of the net score.
#This creates a greater difference between good and bad strategies.
def fitness_score_quadratic(strat,num_trials,alpha):
	score=0
	for i in range(0,num_trials):
		score += play_one_game(strat)
	#Fitness scores should be positive, so normalize to a minimum of 0.
	return max(0,alpha*score*abs(score)+pow(2*num_trials,2))

#Example usage
#s = generate_strategy()
#print fitness_score_linear(s,1000,1)
#print fitness_score_quadratic(s,1000,15)
