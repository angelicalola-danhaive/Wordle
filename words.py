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
		
		Compute an element-wise comparison of two strings to return a reponse array 
		
		Parameters
		----------
		guess
			the guess offered by the user
		solution
			the answer to be compared to the guess

		Returns
		----------
		reponse
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


	
