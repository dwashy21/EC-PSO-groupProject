import math
from random import *
from blackjack import *
from strategy import *
from fitness import *

# strat[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
def main():
    populationSize = 16 #must be (>=2)
    numGenerations = 100 #number of times parents are selected and offspring produced
    numTrials = 1000 #number of times a population member is tested to determine fitness
    numTrialsAlpha = 1 #
    offspringAlpha = .5 #
    mutateAlpha = .8 #

    generations = []
    generations.append(Generation())
    generations[0].population = initializePopulation(populationSize)
    for i in range(0,numGenerations):
        scorePopulationFitness(generations[i], numTrials, numTrialsAlpha)
        printGenerationInfo(generations[i])
        #generations[i].printPopulation()
        parents = selectParents(generations[i])
        #print parents[-1].fitness
        #print parents[-2].fitness
        offspring = generateOffspring(parents, 0, offspringAlpha)
        offspring = mutate(offspring, mutateAlpha)
        generations.append(prepareNextGeneration(Generation(), parents, offspring, i+1)) #pass forward new generation


def mutate(offspring,alpha):
    for o in offspring:
        for dealer_card in range(0, 10): #Ace to Ten. JQK counts as the same as 10.
            for num_points in range(0, 21): #0 to 20 points
                for num_aces in range(0, 5): #0 to 4 aces
                    for num_two_to_five in range(0, 9): #0 to 8 in this category
                        for num_six_to_nine in range(0, 4): #0 to 3 in this category
                            for num_faces in range(0, 3): #0 to 2 faces
                                pivot = random.random()
                                if(alpha > pivot):
                                    (o.strategy)[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces] = Blackjack_Strategy()
    return offspring
        


def prepareNextGeneration(nextGen, parents, offspring, genCount):
    nextGen.population = parents + offspring

    nextGen.generationCount = genCount
    return nextGen

# params:
#   method
#       0 = For each parent, and for each entry in parent's matrix, generate a random num. If random num < alpha, then swap the two
#       1 = Pick a random number for each index in the matrix. For each of those random pick greater or less than that index. If entry index satisfy the picked random numbers and > or <, then swap between the two strategies
def generateOffspring(parents, method, alpha):
    offspring = []
    if(method == 0):
        offspring = offspringFromAlphaSwap(parents, alpha)
    elif(method == 1):
        print 'method 1 not yet complete'
    return offspring

# iterate through every index of strategy matrix, swapping respective values if randomly generated num is < alpha
# STRATEGY : For each parent, and for each entry in parent's matrix, generate a random num. If random num < alpha, then swap the two
def offspringFromAlphaSwap(parents, alpha):
    i = 0
    offspring = []
    while(i < len(parents)): #if iterating through parents, upper bound should be num of pairs
        samp = random.sample(parents, 2)
        mother = samp[0]
        father = samp[1]
        childOne = samp[0].copy() #first child is base copy of 'mother'
        childTwo = samp[1].copy() #second child is base copy of 'father'
        for dealer_card in range(0, 10): #Ace to Ten. JQK counts as the same as 10.
            for num_points in range(0, 21): #0 to 20 points
                for num_aces in range(0, 5): #0 to 4 aces
                    for num_two_to_five in range(0, 9): #0 to 8 in this category
                        for num_six_to_nine in range(0, 4): #0 to 3 in this category
                            for num_faces in range(0, 3): #0 to 2 faces
                                pivot = random.random()
                                if(alpha > pivot):
                                    motherGene = (mother.strategy)[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
                                    fatherGene = (father.strategy)[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
                                    (childOne.strategy)[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces] = fatherGene
                                    (childTwo.strategy)[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces] = motherGene
        offspring.append(childOne)
        offspring.append(childTwo)

        i += 2 #iterate in multiples of 2
    return offspring

def selectParents(generation):
    parents = []
    sortedPopulation = sorted(generation.population, key=getMemberFitness,reverse=True) #sort by fitness (lowest to highest)
    numParents = len(generation.population)/2 #select 50% from
    if(numParents % 2 == 1): #if 'odd' num parents, make even num. We are extracting upper percentile of parents in regards to fitness, so we do not lose best strategy
        numParents -= 1
    for member in sortedPopulation[0:numParents]: #select the most fit, upper 50% of population
        parents.append(member)
    return parents

# used for selectParents() function
def getMemberFitness(member):
    return member.fitness

def scorePopulationFitness(generation, numTrials, alpha):
    maxFitness = float(0.00)
    sumFitness = float(0.00)
    population = generation.population
    for member in population:
        if member.fitness==0:
            member.fitness = fitness_score_linear(member.strategy, numTrials, alpha) #compute fitness for individual member
        if(member.fitness > maxFitness): #check if new max fitness
            maxFitness = member.fitness
        sumFitness += member.fitness #rolling sum for avg fitness
    generation.maxFitness = maxFitness
    generation.avgFitness = sumFitness/float(len(population))

def initializePopulation(populationSize):
    population = []
    for i in range(0, populationSize):
        member = Population_Member()
        member.strategy = generate_strategy()
        population.append(member)

    return population

def printPopulation(population):
    print 'Population (size = %d)' % len(population)
    for member in population:
        print member.fitness

    print '**** end population ****\n'

def printGenerationInfo(generation):
    print 'generation %d:' % (generation.generationCount)
    print '\tmaxFitness = %f' % generation.maxFitness
    print '\tavgFitness = %f' % generation.avgFitness
    print '\tsize = %d' % len(generation.population)

class Population_Member:
    def __init__(self):
        self.fitness = float(0.00)
        self.avgFitness = float(0.00)
        self.generationsLived = 0

    def copy(self):
        newMember = Population_Member()
        newMember.strategy = self.strategy
        return newMember

    def getAverageFitness(self):
        print 'alive'

class Generation:
    def __init__(self):
        self.maxFitness = float(0.00)
        self.avgFitness = float(0.00)
        self.generationCount = 0

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
