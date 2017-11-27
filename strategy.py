import numpy as np
from random import random

class Blackjack_Strategy:
	double_rate = 0.0
	hit_rate = 0.0
	stand_rate = 0.0
	def __init__(self):
		self.double_rate = 0.0#random()
		self.hit_rate = random()
		self.stand_rate = random()

	def __add__(self, other):
		self.double_rate += other.double_rate
		self.hit_rate += other.hit_rate
		self.stand_rate += other.stand_rate

	def __sub__(self, other):
		self.double_rate -= other.double_rate
		self.hit_rate -= other.hit_rate
		self.stand_rate -= other.stand_rate

	def __mul__(self, constant):
		self.double_rate *= constant
		self.hit_rate *= constant
		self.stand_rate *= constant

	def __str__(self):
		return "d" + str(self.double_rate) + " h" + str(self.hit_rate) + " s" + str(self.stand_rate)

	def decision(self):
		total= self.double_rate+self.hit_rate+self.stand_rate
		decision = random()
		if decision < (self.double_rate)/total:
			return 'D'
		elif decision < (self.double_rate+self.hit_rate)/total:
			return 'H'
		else:
			return 'S'


# Remember everything has to be minus one, since arrays start at 0.
# strat[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
def generate_strategy():
	dealer_card_array = np.full((10,21,95,9,4,3),Blackjack_Strategy(),object)
	for dealer_card in range(0,10):#Ace to Ten. JQK counts as the same as 10.
		#num_points_array = []
		for num_points in range(0,21):#0 to 20 points
			#num_aces_array = []
			for num_aces in range(0,5):#0 to 4 aces
				#num_two_to_five_array = []
				for num_two_to_five in range(0,9): #0 to 8 in this category
					#num_six_to_nine_array = []
					for num_six_to_nine in range(0,4):#0 to 3 in this category
						#num_faces_array = []
						for num_faces in range(0,3):#0 to 2 faces
							dealer_card_array[dealer_card][num_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]=Blackjack_Strategy()
							#num_faces_array.append(Blackjack_Strategy())
						#num_six_to_nine_array.append(num_faces_array)
					#num_two_to_five_array.append(num_six_to_nine_array)
				#num_aces_array.append(num_two_to_five_array)
			#num_points_array.append(num_aces_array)
		#dealer_card_array.append(num_points_array)
	return dealer_card_array

#s = generate_strategy()
#print s[0][5][0][2][0][0]
