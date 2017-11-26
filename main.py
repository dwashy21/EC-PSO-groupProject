from blackjack import *
from strategy import *
from fitness import *

# strat[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
def main():
    population = []
    populationSize = 20
    numGenerations = 100

    print 'Initializing population...'
    for i in range(0, populationSize):
        member = Population_Member()
        member.strategy = generate_strategy()
        population.append(member)

    print 'Initial population created.'
    for member in population:
        member.fitnessScores = fitness_scores(member.strategy, numGenerations)

    for member in population:
        print member.computeAvgFitness()


    #print strategy[0][5][0][2][0][0]
    #print strategy[0][5][0][2][1][0]



class Population_Member:
    def __init__(self):
        self.fitnessScores = []

    def computeAvgFitness(self):
        numScores = len(self.fitnessScores)
        avg = float(0.00)
        for score in self.fitnessScores:
            avg += float(score)
        self.avgFitness = avg/(float(numScores))
        return self.avgFitness


"""
Init
"""
if __name__ == "__main__":
    main()
