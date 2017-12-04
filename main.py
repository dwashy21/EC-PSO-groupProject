import math
from random import *
from blackjack import *
from strategy import *
from fitness import *
from plot import *


# strat[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
def main():
    populationSize = 10 #must be (>=2)
    numGenerations = 10 #number of times parents are selected and offspring produced
    numTrials = 1000 #number of times a population member is tested to determine fitness
    numTrialsAlpha = 1 #NOTE try, .
    offspringAlpha = .5 #NOTE: try ..2, .5, .7, .9
    mutateAlpha = .5 #NOTE: try .2, .5, .7, .9

    parentSelectionMethods = ['mu+lambda', 'mu,lambda', 'r']
    selMethod = parentSelectionMethods[1];

    maxFitness = [-1]
    avgFitness = []
    generations = []
    generations.append(Generation())
    generations[0].population = initializePopulation(populationSize)
    for i in range(0,numGenerations):
        scorePopulationFitness(generations[i], numTrials, numTrialsAlpha)
        parents = selectParents(generations[i], selMethod)
        offspring = createOffspring(selMethod, parents, offspringAlpha, i+1)
        offspring = mutate(offspring, mutateAlpha)
        nextGeneration = prepareNextGeneration(Generation(), parents, offspring, i+1, selMethod)
        generations.append(nextGeneration) #pass forward new generation
        maxFitness.append(getMaxFitness(generations[i], maxFitness[i]))
        avgFitness.append(generations[i].avgFitness)
        printGenerationInfo(generations[i])

    n = numGenerations-1
    createPlot(maxFitness, avgFitness)
    writeSummary(selMethod, maxFitness[n], avgFitness[n], offspringAlpha, mutateAlpha)

def writeSummary(method, maxF, avgF, offspringAlpha, mutateAlpha):
    file = open('method_'+str(method)+'-'+str(random.random())+'.txt', 'w');
    file.write('method: '+str(method)+'\n')
    file.write('maxF: '+str(maxF)+'\n')
    file.write('avgF: '+str(avgF)+'\n')
    file.write('offspringAlpha: '+str(offspringAlpha)+'\n')
    file.write('mutateAlpha: '+str(mutateAlpha)+'\n')
    file.close()

def getMaxFitness(generation, universalMax):
    if(generation.maxFitness > universalMax):
        return generation.maxFitness
    else:
        return universalMax

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


def selectParents(generation, method):
    parents = []
    numParents = len(generation.population)/2 #select 50% from
    if(numParents % 2 == 1): #if 'odd' num parents, make even num. We are extracting upper percentile of parents in regards to fitness, so we do not lose best strategy
        numParents -= 1

    if(method=='mu,lambda'):
        for member in generation.population:
            if(member.generationCount == generation.generationCount):
                parents.append(member)
    elif(method=='mu+lambda'):
        sortedPopulation = sorted(generation.population, key=getMemberFitness,reverse=True) #sort by fitness (lowest to highest)
        for member in sortedPopulation[0:numParents]: #select the most fit, upper 50% of population
            parents.append(member)

    return parents


def createOffspring(method, parents, alpha, offspringGen):
    if('mu' in method):
        return createCrossoverOffspring(parents, alpha, offspringGen)
    elif(method=='r'):
        print 'here'

# iterate through every index of strategy matrix, swapping respective values if randomly generated num is < alpha
# STRATEGY : For each parent, and for each entry in parent's matrix, generate a random num. If random num < alpha, then swap the two
def createCrossoverOffspring(parents, alpha, offspringGeneration):
    i = 0
    offspring = []
    while(i < len(parents)): #if iterating through parents, upper bound should be num of pairs
        samp = random.sample(parents, 2)
        mother = samp[0]
        father = samp[1]
        childOne = samp[0].copy() #first child is base copy of 'mother'
        childTwo = samp[1].copy() #second child is base copy of 'father'
        childOne.generationCount = offspringGeneration
        childTwo.generationCount = offspringGeneration
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

def prepareNextGeneration(nextGen, parents, offspring, genCount, selMethod):
    if(selMethod == 'mu,lambda'):
        nextGen.population = offspring
        nextGen.generationCount = genCount
    elif(selMethod == 'mu+lambda'):
        nextGen.population = parents + offspring
        nextGen.generationCount = genCount

    return nextGen


# used for selectParents() function
def getMemberFitness(member):
    return member.fitness

def getOnlyOffspringFromPopulation(generation):
    offspring = []
    pop = generation.population
    for p in pop:
        if (p.generation == generation.generationCount):
            offspring.append(p)

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
        self.generationCount = 0 #which generation this member originated, indexed from 0

    def copy(self):
        newMember = Population_Member()
        newMember.strategy = self.strategy
        return newMember

    def setOriginGeneration(self, gen):
        self.generation = gen

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
