import random
from strategy import *
from fitness import *
import numpy as np
import time

#Constants for updating velocities
C1=0.75
C2=3.25
NUM_TRIALS=1000
NUM_TRIALS_ALPHA=1

#A class representing a particle
class Particle:

	def __init__(self,index,num_particles):
		self.index = index
		self.num_particles = num_particles
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
		for d in range(0,10):#Ace to Ten. JQK counts as the same as 10.
			for p in range(0,21):#0 to 20 points
				for a in range(0,5):#0 to 4 aces
					for t in range(0,9): #0 to 8 in this category
						for s in range(0,4):#0 to 3 in this category
							for f in range(0,3):#0 to 2 faces
								v=self.velocity[d,p,a,t,s,f]
								r1=random.random()
								r2=random.random()
								alpha_h=(self.personal_best[d][p][a][t][s][f].hit_rate-self.position[d][p][a][t][s][f].hit_rate)*r1*C1
								beta_h=(neighbor_best.position[d][p][a][t][s][f].hit_rate-self.position[d][p][a][t][s][f].hit_rate)*r2*C2	
								alpha_s=(self.personal_best[d][p][a][t][s][f].stand_rate-self.position[d][p][a][t][s][f].stand_rate)*r1*C1
								beta_s=(neighbor_best.position[d][p][a][t][s][f].stand_rate-self.position[d][p][a][t][s][f].stand_rate)*r2*C2	
								
								self.velocity[d][p][a][t][s][f].hit_rate=v.hit_rate+alpha_h+beta_h
								self.velocity[d][p][a][t][s][f].stand_rate=v.stand_rate+alpha_s+beta_s

	def update_position(self):
		for d in range(0,10):#Ace to Ten. JQK counts as the same as 10.
			for p in range(0,21):#0 to 20 points
				for a in range(0,5):#0 to 4 aces
					for t in range(0,9): #0 to 8 in this category
						for s in range(0,4):#0 to 3 in this category
							for f in range(0,3):#0 to 2 faces
								self.position[d][p][a][t][s][f].hit_rate = self.position[d][p][a][t][s][f].hit_rate+self.velocity[d][p][a][t][s][f].hit_rate
								self.position[d][p][a][t][s][f].stand_rate = self.position[d][p][a][t][s][f].stand_rate+self.velocity[d][p][a][t][s][f].stand_rate

		self.fitness=fitness_score_points(self.position,NUM_TRIALS,NUM_TRIALS_ALPHA)
		if self.fitness>self.personal_best_fitness:
			self.personal_best=self.position
			self.personal_best_fitness=self.fitness


	#Topologies: 1-star, 2-ring
	def get_neighborhood_best(self,topology, particles):
		if topology == 1:
			s=sorted(particles, key=getFitness,reverse=True)
			return s[0]
		else: 	
			i=self.index
			left_fit=particles[i-1].fitness
			self_fit=particles[i].fitness
			right_fit=particles[(i+1)%len(particles)].fitness
			max_fit=max(left_fit,self_fit,right_fit)
			if max_fit==left_fit:
				return particles[i-1]
			elif max_fit==self_fit:
				return particles[i]
			else:
				return particles[(i+1)%len(particles)]

def particle_swarm_optimization():
	t = time.time()
	NUM_PARTICLES = 10
	MAX_GEN=100
	particles = [Particle(i,NUM_PARTICLES) for i in range(0,NUM_PARTICLES)]
	best_fitness_history = []
	avg_fitness_history = []

	for gen in range(0,MAX_GEN):
		print "Gen:" + str(gen)
		t=time.time()
		for j in range(0,NUM_PARTICLES):
			particles[j].update_velocity(particles[j].get_neighborhood_best(2,particles))
			particles[j].update_position()
		best=sorted(particles, key=getFitness,reverse=True)[0]
		best_fitness_history.append(best.fitness)
		avg_fitness_history.append(getAvgFitness(particles))
		print best.fitness 
		print avg_fitness_history[-1]
		print time.time() - t


	best=sorted(particles, key=getBestFitness,reverse=True)[0]

def getFitness(particle):
	return particle.fitness

def getBestFitness(particle):
	return particle.personal_best_fitness

def getAvgFitness(particles):
	avg = 0
	for particle in particles:
		avg+=particle.fitness
	avg /= len(particles)
	return avg

print 'start\n'
t = time.time()
particle_swarm_optimization()
print time.time()-t