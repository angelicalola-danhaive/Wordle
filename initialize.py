"""
	This Module contains functions needed to initialize the game. They will all be used in one big function (defined at the end of this module) that is called at the very start
	of the wordle_solver.py
	
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""

import numpy as np
from wordfreq import word_frequency, zipf_frequency #zipf_frequency gives the freqs of a human-friendly logarithmic scale, they range from 0-8

def compute_all(words_list):
	'''
		Function that assings a word a score based on how probable it is that it's the answer + a frequency in the english language
		Will be used at the beginning suring initialization of the game (only computed once)

		Parameters
		----------
		words_list
			list of all of possible words so far

		Returns
		----------
		scores
			an array with the score given to each word, in the order of the words appearing on the words_list
		word_frequenciesfrequencies
			array with the frequency of each word in the order that they appear in words_list
	'''
	scores = np.zeros(len(words_list))
	word_frequencies = np.zeros(len(words_list))

	frequencies = compute_letter_frequencies(words_list)

	#for each word in the list, get the score by: summing over the total freqs of each letter in the word + the freq of the spot that it is in

	for word_index,word in enumerate(words_list):
		word_array = list(word)
		#fill out the freq array
		word_frequencies[word_index] = zipf_frequency(word,'en')

		#fill out the scores array, giving it zero directly if it has repeated letters since that makes it a bad first guess (because we get less info)
		if len(np.unique(word_array)) != len(word_array): #if there's one or more non-unique letters in the word, directly move on to next word
			break
		for letter_index,letter in enumerate(word_array):
			index = ord(letter) - 97
			scores[word_index]+= (frequencies[index,0] + frequencies[index,letter_index+1])

	return scores, word_frequencies

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

	#count how many times each letter appears in each position

	for word in words_list:
		word_array = list(word)
		for position,letter in enumerate(word_array):
			index = ord(letter) - 97 #-96 gives a = 1, but our array starts at index 0 so a=0, meaning we need to substract 97
			frequencies[index,position+1]+= 1 #position+1 because j=0 is the overall frequency in words
	for i in range(26): #to go through all of the letters
		frequencies[i,0] = np.sum(frequencies[i,1:6]) #compute how much it appears in total
		
	return frequencies
