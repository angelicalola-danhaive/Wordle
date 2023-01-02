"""
	This Module contains functions needed to initialize the game. They will all be used in one big function (defined at the end of this module) that is called at the very start
	of the wordle_solver.py
	
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""

import numpy as np

def compute_probabilities(words_list):
	'''
		Function that assings a word a score based on how probable it is that it's the answer
		Will be used at the beginning suring initialization of the game (only computed once)

		Parameters
		----------
		words_list
			list of all of possible words so far

		Returns
		----------
		probabilities
			an array with the score given to each word, in the order of the words appearing on the list
	'''

	return probabilities

def compute_letter_frequencies(words_list):
	'''
		Function that computes the frequency of each letter in a 5 letter word and in each position
		Will be in compute_probabilities

		Parameters
		----------
		words_list
			list of all of possible words so far

		Returns
		----------
		frequencies
			2D array [i,j] with i,0 the frequency of the ith letter in a 5 letter word, and i,j>0 the frequency of the ith letter in the jth position
	'''
	frequencies = np.zeros((26,6))

	for word in words_list:
		word_array = list(word)
		for position,letter in enumerate(word_array):
			index = ord(letter) - 97 #-96 gives a = 1, but our array starts at index 0 so a=0, meaning we need to substract 97
			frequencies[index,position+1]+= 1 #position+1 because j=0 is the overall frequency in words
	for i in range(26): #to go through all of the letters
		frequencies[i,0] = np.sum(frequencies[i,1:6])
		
	return frequencies