from strategy import *

import random
import itertools

#Creates a deck of cards by the cross product of suits and ranks.
SUITS = 'cdhs'
RANKS = '23456789TJQKA'
DECK = tuple(''.join(card) for card in itertools.product(RANKS, SUITS))
CARD_VALUES = { "A":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10, "J":10, "Q":10, "K":10 }


def update_hand(card, num_card_value):
	card_value = card[0]#The first character tells us the card value
	
	if card_value in "A":
		num_card_value["A"]=num_card_value["A"]+1
	elif card_value in "2345":		
		num_card_value["2345"]=num_card_value["2345"]+1
	elif card_value in "6789":		
		num_card_value["6789"]=num_card_value["6789"]+1
	elif card_value in "TJQK":		
		num_card_value["TJQK"]=num_card_value["TJQK"]+1

#Gives number of points given hand.
def hand_points(cards):
	num_aces=0
	points=0
	for card in cards:
		points+=CARD_VALUES[card[0]]
		if card[0] in "A":
			num_aces+=1

	while points > 21 and num_aces > 0:
		num_aces-=1
		points-=10

	return points

#Plays one game of blackjack given the strategy.
def play_one_game(bj_strat):
	#By using a random sample, we are effectively shuffling the deck.
	hand = random.sample(DECK, 52)
	dealer_card=0
	my_points=0
	num_card_value={"A":0,"2345":0,"6789":0,"TJQK":0}
	decision='H' 
	deck_counter=0
	doubledown=1 #Multiplier of 2 if player doubled down.

	#Deal initial hand
	my_cards=[]
	deal_cards=[]

	my_cards.append(hand[0])
	update_hand(hand[0], num_card_value)

	deal_cards.append(hand[1])#This is hidden from the player initially.

	my_cards.append(hand[2])
	update_hand(hand[2], num_card_value)
	my_points=hand_points(my_cards)

	deal_cards.append(hand[3])
	dealer_card=(CARD_VALUES[hand[3][0]]-1)%10

	deck_counter=4

	# 'H'-hold, 'S'-stand, 'D'-doubledown
	# strat[dealer_card][my_points][num_aces][num_two_to_five][num_six_to_nine][num_faces]
	if my_points < 21:
		decision=bj_strat[dealer_card][my_points][num_card_value["A"]][num_card_value["2345"]][num_card_value["6789"]][num_card_value["TJQK"]].decision()
	else:
		decision='S'

	#Deal a card based on decision as long as not busting 
	while my_points < 21 and decision!='S':
		my_cards.append(hand[deck_counter])
		update_hand(hand[deck_counter], num_card_value)
		my_points=hand_points(my_cards)
		if decision=='D':
			doubledown=2
			decision='S' #Must stand after doubling.
		elif my_points < 21:
			decision=bj_strat[dealer_card][my_points][num_card_value["A"]][num_card_value["2345"]][num_card_value["6789"]][num_card_value["TJQK"]].decision()

		deck_counter+=1

	#Dealer's turn
	dealer_points=hand_points(deal_cards)
	while dealer_points <= 17:
		deal_cards.append(hand[deck_counter])
		dealer_points=hand_points(deal_cards)
		deck_counter+=1

	#Determine winner
	if my_points > 21:
		return -1*doubledown
	elif dealer_points > 21:
		return doubledown
	elif my_points==21 and len(my_cards)==2 and (dealer_points < 21 or len(deal_cards)>2):
		return doubledown*1.5 #A blackjack pays out 3:2
	elif my_points < dealer_points:
		return -1*doubledown
	elif my_points > dealer_points:
		return doubledown
	else:
		return 0 #Tied
