import math
from blackjack import *
from strategy import *
from fitness import *

# strat[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
def main():
    populationSize = 20 #must be (>=2)
    numGenerations = 10 #number of times parents are selected and offspring produced
    numTrials = 100 #number of times a population member is tested to determine fitness
    alpha = .5 #

    generations = []
    generations.append(Generation())
    generations[0].population = initializePopulation(populationSize)
    for i in range(0,numGenerations):
        #create next generation from existing one
        nextGen = Generation()
        scorePopulationFitness(generations[i], numTrials, alpha)
        parents = selectParents(generations[i])
        #nextGen.population = generateOffspring(parents)
        #generations.append(nextGen) #pass forward new generation
        break

#def generateOffspring(parents):


def selectParents(generation):
    parents = []
    sortedPopulation = sorted(generation.population, key=getMemberFitness) #sort by fitness (lowest to highest)
    numParents = len(generation.population)/2 #select 50% from
    if(len(generation.population) % 2 == 1): #if 'odd' num parents, make even num
        numParents -= 1
    for member in sortedPopulation[numParents-1:-1]: #select the most fit, 50% of population
        parents.append(member)

    return parents

def getMemberFitness(member):
    return member.fitness

def scorePopulationFitness(generation, numTrials, alpha):
    maxFitness = float(0.00)
    sumFitness = float(0.00)
    population = generation.population
    for member in population:
        member.fitness = fitness_score_linear(member.strategy, numTrials, alpha) #compute fitness for individual member
        if(member.fitness > maxFitness): #check if new max fitness
            maxFitness = member.fitness
        sumFitness += member.fitness #rolling sum for avg fitness
    generation.maxFitness = maxFitness
    generation.avgFitness = sumFitness/float(len(population))

def initializePopulation(populationSize):
    population = []
    print 'Initializing population...'
    for i in range(0, populationSize):
        member = Population_Member()
        member.strategy = generate_strategy()
        population.append(member)

    print 'Initial population created.'
    return population

def printPopulation(population):
    print 'Population (size = %d)' % len(population)
    for member in population:
        print member.fitness

    print '**** end population ****\n'

class Population_Member:
    def __init__(self):
        self.fitness = float(0.00)
        self.avgFitness = float(0.00)
        self.generationsLived = 0

class Generation:
    def __init__(self):
        self.maxFitness = float(0.00)
        self.avgFitness = float(0.00)

    def printPopulation(self):
        print 'Population (size = %d)' % len(self.population)
        for member in self.population:
            print member.fitness

        print '**** end population ****\n'


"""
Init
"""
if __name__ == "__main__":
    main()
