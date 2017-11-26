from blackjack import *
from strategy import *
from fitness import *

# strat[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
def main():
    population = []
    populationSize = 20
    numGenerations = 100 #number of times parents are selected and offspring produced
    numTrials = 100 #number of times a population member is tested to determine fitness
    alpha = .5 #

    print 'Initializing population...'
    for i in range(0, populationSize):
        member = Population_Member()
        member.strategy = generate_strategy()
        population.append(member)

    print 'Initial population created.'
    for member in population:
        print fitness_score_linear(member.strategy, numTrials, alpha)

    #for member in population:
        #print member.fitness


    #print strategy[0][5][0][2][0][0]
    #print strategy[0][5][0][2][1][0]



class Population_Member:
    def __init__(self):
        self.fitness = float(0.00)



"""
Init
"""
if __name__ == "__main__":
    main()
