"""
	This Module contains functions that analyze the word list to compute different scores for the words based on selection criteria.
	
	Contains:
	----------------------------------------
	compute_all
		computes the score for each word in the list, outputs the corresponding array
	compute_letter_frequencies
		computes the frequency of each letter in terms of its appearence in words from words_list
	compute_difference_score
		computes the amount of different letters between each word in words_list and the guess
	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""

#imports
import numpy as np
import words

def compute_all(words_list, first = False):
	'''
		Function that assings a word a score based on the frequencies of the letters it contains

		Parameters
		----------
		words_list
			list of all of possible words so far
		first
			boolean indicating if we are at the first guess (True) or not (False)

		Returns
		----------
		scores
			an array with the score given to each word, in the order of the words appearing on the words_list
	'''
	#initialize the array
	scores = np.zeros(len(words_list))

	#compute the frequency of each letter in the words of words_list
	frequencies = compute_letter_frequencies(words_list)

	#for each word in the list, get the score by summing over the frequency of each letter in the word 
	for word_index,word in enumerate(words_list):
		word_array = list(word)
		unique = len(np.unique(word_array))

		#penalize words with repeated letters for the first guess
		if first and unique!= 5: #if there's one or more non-unique letters in the word, directly move on to next word (meaning this word gets a score of zero)
			continue

		for letter_index,letter in enumerate(word_array):
			index = ord(letter) - 97
			#sum over frequency in words and frequency in that given position
			scores[word_index]+= (frequencies[index,0] + frequencies[index,letter_index+1])
		scores[word_index] = scores[word_index]/(10*(6-unique)) #reduce score of double letters

	return scores


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
		for position, letter in enumerate(word):
			index = ord(letter) - 97 #-96 gives a = 1, but our array starts at index 0 so a=0, meaning we need to substract 97
			frequencies[index,position+1]+= 1 #position+1 because j=0 is the overall frequency in words
			frequencies[index,0]+= 1
	return frequencies


def compute_difference_score(words_list,guess):
	'''
		Function that computes a score based on how many letters differ between the guess and each word in words_list

		Parameters
		----------
		words_list
			list of all of possible words so far
		guess
			the previous guess 

		Returns
		----------
		difference_score
			array with the difference score assigned to each word
	'''
	difference_score = np.zeros(len(words_list))
	
	for index,word in enumerate(words_list):
		difference = words.count_difference(list(word),list(guess))
		difference_score[index] = difference

	return difference_score
