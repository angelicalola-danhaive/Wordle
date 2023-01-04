"""
	This Module contains functions to use and compare words.
	
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""

import numpy as np

def compare(guess,solution):
	"""
		Comparing the characters of 2 words given as input
		
		Compute an element-wise comparison of two strings to return a response array 
		
		Parameters
		----------
		guess
			the guess offered by the user
		solution
			the answer to be compared to the guess

		Returns
		----------
		response
			the array of colors corresponding to how correct the letters in the guess are
			the colors are 'B' for black (letter not in word), 'Y' for yellow (letter in word but wrong place), 'G' for green (letter in the right place)
	"""
	response = list(['B','B','B','B','B'])

	#turn the array into a list so that it's easier for operations
	guess_array = list(guess)
	solution_array = list(solution)

	#element wise comparison with np.compare_chararrays() => outputs a bool array with True if the right letter is in the right place (so you also have the indices)
	#=> those will directly be green
	green_letters = np.char.compare_chararrays(guess_array, solution_array,'==',rstrip = True )


	# the letters that match get removed so we can focus on the yellow ones
	for i,letter in enumerate(green_letters):
		if letter:
			guess_array[i] = '*'
			solution_array[i] = '**'

	#use np.interset1d to get letters that are in both + their indices in both letters
	yellow_letters, index_guess,index_solution = np.intersect1d(guess_array,solution_array,return_indices=True)

	#fill out response array using the green and yellow letter arrays
	for i in range(len(response)):
		if green_letters[i]:
			response[i] = 'G'
		if i<len(yellow_letters) and index_guess[i] != index_solution[i]:
			response[index_guess[i]] = 'Y'

	return response


def sort(words_list,frequencies,guess,response):
	'''
		Sorting the list of words by:
		 1. removing all options that don't match the response array of colors (i.e. don't have letters in the right place)
		 2. sorting the remaining ones by probabilities

				Parameters
		----------
		words_list
			list of all of possible words so far
		guess
			the guess that was tested by the compare function
		response
			the response array of colors, result of the compare function

		Returns
		----------
		new_list
			new list of words that match the given response colors
		new_frequencies
			new list of the frequencies for the words on new_list

	'''
	new_list = []
	new_frequencies = []

	green_letters = []
	green_indices = []

	yellow_letters = []
	yellow_indices = []

	black_letters = []

	#sort through the letters to make the sorting through the words easier
	for index,letter in enumerate(list(guess)):
		if response[index] == 'G':
			green_letters.append(letter)
			green_indices.append(index)
		if response[index] == 'Y':
			yellow_letters.append(letter)
			yellow_indices.append(index)
		if response[index] == 'B':
			black_letters.append(letter)

	#check which words have all the greens in right spot, have the yellows NOT in the same spot as the guess but still in the word, and don't have blacks
	for index,word in enumerate(words_list):
		keep = check_word(list(word), green_letters,green_indices, yellow_letters, yellow_indices, black_letters)
		if keep: 
			new_list.append(word)
			new_frequencies.append(frequencies[index])
	return new_list, new_frequencies

def check_word(word,green_letters,green_indices, yellow_letters, yellow_indices, black_letters):
	'''
		Checking if a word matches the response array obtained from the guess

				Parameters
		----------
		word
			word that we want to test, array
		green_letters, green_indices
			arrays with the green letters and their place in the word
		yellow_letters, yellow_indices
			arrays with the yellow letters and their place in the word
		black_letters
			array with the black letters

		Returns
		----------
		bool
			a boolean indicating if the word matches the reponse (True) or doesn't and should hence be removed from the list (False)
	'''	
	#check which words have all the greens in right spot, have the yellows NOT in the same spot as the guess but still in the word, and don't have blacks
	#see if this loop can be improved on!

	if len(green_letters)!= 0:
		for i in range(len(green_letters)):
			if word[green_indices[i]] != green_letters[i]:
				return False

	if len(yellow_letters)!= 0:
		for i in range(len(yellow_letters)):
			if word[yellow_indices[i]] == yellow_letters[i] or (yellow_letters[i] not in word):
				return False			

	if len(black_letters)!= 0:
		for i in range(len(black_letters)):
			#account for double letters in the guess but only one is in the answer (meaning all words with two occurences of that letter must be eliminated)
			if ( (black_letters[i] in green_letters) or (black_letters[i] in yellow_letters) ):
				if word.count(black_letters[i])>1: 
					return False
				else:
					return True

			elif black_letters[i] in word :
				return False
	#if all checks have passed then return True 
	return True	

def count_difference(guess2, guess1):
	'''
		Counting how many letters differ between two words

				Parameters
		----------
		guess1
		guess2
			the two words we want to compare. guess 1 is the previous guess and guess2 is the word being tested to be guessed next

		Returns
		----------
		different
			int of the number of letters differring from word1 and word2
	'''
	#want to only count each letter once so only take unique values from guess 2
	guess2_unique = np.unique(list(guess2))
	#returns an array len(word1) that is true when a char in guess2 is in guess1 and false other wise => we can count the False to get difference
	repetition = np.isin(guess2_unique,list(guess1))
	different = np.sum(np.invert(repetition)) #sum over the false values so need to invert because np.sum counts the True values
	return different 

def verify(word):
	'''
		Check that the word given as input is a valid wordle word

				Parameters
		----------
		word
		words_list
			the list of possible wordle words
		Returns
		----------
		word
			word that has been checked
	'''
	#compute the words list
	with open('WordleWords.txt') as file:
		words_list = [line.rstrip() for line in file] 
	#check if input is correct
	correct = False
	while not correct:
		if word.lower() not in words_list:
			word = input('Error: Invalid word! Please provide another 5 letter word: ')
		else: 
			return word
