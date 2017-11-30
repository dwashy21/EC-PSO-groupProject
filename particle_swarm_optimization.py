import random
from strategy import *
from fitness import *
import numpy as np
import time

#Constants for updating velocities
C1=1.1
C2=2.8
NUM_TRIALS=1000
NUM_TRIALS_ALPHA=1

#A class representing a particle
class Particle:

	def __init__(self):
		self.position=generate_strategy()
		self.fitness=fitness_score_points(self.position,NUM_TRIALS,NUM_TRIALS_ALPHA)
		self.velocity=generate_strategy()
		for dealer_card in range(0,10):#Ace to Ten. JQK counts as the same as 10.
			for num_points in range(0,21):#0 to 20 points
				for num_aces in range(0,5):#0 to 4 aces
					for num_two_to_five in range(0,9): #0 to 8 in this category
						for num_six_to_nine in range(0,4):#0 to 3 in this category
							for num_faces in range(0,3):#0 to 2 faces
								a=self.velocity[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
								self.velocity[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]=a.random_velocity()
							
		self.personal_best=self.position.copy()
		self.personal_best_fitness=self.fitness

	def update_velocity(self,neighbor_best):	
		#self.velocity = self.velocity+(self.personal_best-self.position)*random.random()*C1+(neighbor_best.position-self.position)*random.random()*C2
		for d in range(0,10):#Ace to Ten. JQK counts as the same as 10.
			for p in range(0,21):#0 to 20 points
				for a in range(0,5):#0 to 4 aces
					for t in range(0,9): #0 to 8 in this category
						for s in range(0,4):#0 to 3 in this category
							for f in range(0,3):#0 to 2 faces
								v=self.velocity[d][p][a][t][s][f]
								alpha=(self.personal_best[d][p][a][t][s][f]-self.position[d][p][a][t][s][f])*random.random()*C1
								beta=(neighbor_best.position[d][p][a][t][s][f]-self.position[d][p][a][t][s][f])*random.random()*C2	
								self.velocity[d][p][a][t][s][f]=v+alpha+beta			

	def update_position(self):
		for d in range(0,10):#Ace to Ten. JQK counts as the same as 10.
			for p in range(0,21):#0 to 20 points
				for a in range(0,5):#0 to 4 aces
					for t in range(0,9): #0 to 8 in this category
						for s in range(0,4):#0 to 3 in this category
							for f in range(0,3):#0 to 2 faces
								self.position[d][p][a][t][s][f] = self.position[d][p][a][t][s][f]+self.velocity[d][p][a][t][s][f]
		self.fitness=fitness_score_points(self.position,NUM_TRIALS,NUM_TRIALS_ALPHA)
		if self.fitness>self.personal_best_fitness:
			self.personal_best=self.position
			self.personal_best_fitness=self.fitness


	#Topologies: 1-star, 2-ring
	def get_neighborhood_best(self,topology, particles):
		if topology == 1:
			s=sorted(particles, key=getFitness,reverse=True)
			return s[0]
		else: #Fix this
			s=sorted(particles, key=getFitness,reverse=True)
			return s[0]



def particle_swarm_optimization():
	t = time.time()
	NUM_PARTICLES = 10
	MAX_GEN=100
	particles = [Particle() for i in range(0,NUM_PARTICLES)]


	for gen in range(0,MAX_GEN):
		print "Gen:" + str(gen)
		for j in range(0,NUM_PARTICLES):
			particles[j].update_velocity(particles[j].get_neighborhood_best(1,particles))
			particles[j].update_position()
		best=sorted(particles, key=getFitness,reverse=True)[0]
		print best.fitness
	elapsed = time.time() - t

	best=sorted(particles, key=getBestFitness,reverse=True)[0]
	print best.personal_best_fitness
	print elapsed

def getFitness(particle):
	return particle.fitness

def getBestFitness(particle):
	return particle.personal_best_fitness



particle_swarm_optimization()
