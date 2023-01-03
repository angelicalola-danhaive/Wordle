"""
	This Module contains functions needed to interact with the user and play the game.
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""
import words
import probabilities as proba
import numpy as np

def initialize():
	'''
		Function that initiliazes the game, meaning it runs everything until the first interaction with the user

		Parameters
		----------

		Returns
		----------
		interactive
			bool corresponding to the player' s choice to play the interactive version or not
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word
		frequencies
			frequencies of each word in the english language
		scores_ordered_indices 
			the ordered indices of the words with respect to their score (descending)
	'''
	answer = input('Welcome to the Wordle Solver, would you like to play interactively or ask me to solve for a word? Write INTERACT or SOLVE and press ENTER: ')

	if answer == 'INTERACT' or answer == 'interact' or answer == 'Interact':
		interactive = True
	else:
		interactive = False

	#load of all the words into a list
	with open('WordleWords.txt') as file:
		words_list = [line.rstrip() for line in file] 

	#compute the probabilities of the letters and give the words a score => highest score will be the first guess 
	#(this could also be done separately and the results saved in a txt file.. see how long it takes and then decide)
	scores, frequencies = proba.compute_all(words_list)

	#normalize the frequencies so that they sum to 1 and hence can be used as probabilities
	frequencies = frequencies/frequencies.sum()

	#sort the indices of the words in order from highest to lowest score/frequency (have to flip because function gives them in ascending order and we want descending for simplicity)
	scores_ordered_indices = np.flip(np.argsort(scores))

	return interactive, words_list, scores, frequencies, scores_ordered_indices


def guess_interactive(words_list, scores, frequencies, scores_ordered_indices):
	'''
		Function that makes the user guess until they find the right answer

		Parameters
		----------
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word
		frequencies
			frequencies of each word in the english language
		scores_ordered_indices 
			the ordered indices of the words with respect to their score (descending)

		Returns
		----------
		tries
			the number of guesses until finding the right one
	'''
	tries = 0
	solution_found = False
	#1. the code selects a word at random (the probability p is given by the frequency in the language)
	solution = np.random.choice(words_list,size = None, replace = True, p= frequencies)
	print(solution)
	#2. asks the user for a first guess and provide a suggestion of the best option (based on score)
	suggestion = words_list[scores_ordered_indices[0]] 
	guess = input('Enter your first guess, then press ENTER. I suggest the word {}. '.format(suggestion))
	#3. output the response array of colors
	response = words.compare(guess, solution)
	print('Here are the results from your guess: \n', response[0], response[1],response[2],response[3], response[4])
	# words_list is modified to only include possible words
	words_list,frequencies = words.sort(words_list, frequencies, guess, response)

	#loop until the right word is found
	while not solution_found:
		tries+= 1
		suggestion = words_list[np.argmax(frequencies)]
		guess = input('Guess again and press ENTER. I suggest the word {}. '.format(suggestion))
		response = words.compare(guess, solution)
		print('Here are the results from your guess: \n', response[0], response[1],response[2],response[3], response[4])

		if guess == solution:
			solution_found = True
			break
		words_list,frequencies = words.sort(words_list, frequencies, guess, response)

	return tries, solution
