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

	#normalize the frequencies and scores so that they sum to 1 and hence can be used as probabilities
	frequencies = frequencies/frequencies.sum()
	scores = scores/scores.sum()


	return interactive, words_list, scores, frequencies


def guess_interactive(words_list, scores, frequencies):
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

		Returns
		----------
		tries
			the number of guesses until finding the right one
	'''
	tries = 1
	solution_found = False

	#1. the code selects a word at random (the probability p is given by the frequency in the language)
	solution = np.random.choice(words_list,size = None, replace = True, p= frequencies)
	# print(solution)

	#guess 1 and 2 are chosen differently from the rest so they have written in different sub-functions
	guess, words_list_1,frequencies_1 = guess1(solution,words_list, scores, frequencies)
	tries +=1
	guess, words_list_2,frequencies_2 = guess2(solution,guess,words_list, frequencies)
	#the words_list used is the intersection of the two resulting from the first two guesses
	words_list,indices1,indices2 = np.intersect1d(words_list_1,words_list_2,assume_unique=False, return_indices=True)
	frequencies = np.take(frequencies_1, indices1)
	#renormalize
	frequencies = frequencies/frequencies.sum()

	#loop until the right word is found
	while not solution_found:
		tries+= 1
		suggestion = np.random.choice(words_list,size = None, replace = True, p= frequencies)
		guess = input('Guess again and press ENTER. I suggest the word {}. '.format(suggestion))
		response = words.compare(guess, solution)
		print('Here are the results from your guess: \n', response[0], response[1],response[2],response[3], response[4])

		if guess == solution:
			solution_found = True
			break
		words_list,frequencies = words.sort(words_list, frequencies, guess, response)
		#renormalize because there are less words now
		frequencies = np.array(frequencies)/sum(frequencies)

	return tries, solution

def guess1(solution,words_list, scores, frequencies):
	'''
		Function to run the code for the user's first guess 

		Parameters
		----------
		solution
			of the wordle run
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word
		frequencies
			frequencies of each word in the english language

		Returns
		----------
		guess
			the guess
		words_list
			the list of all words that can still be the answer
		frequencies
			their frequencies
	'''
	#2. asks the user for a first guess and provide a suggestion of the best option (based on score)
	suggestion = suggestion = np.random.choice(words_list,size = None, replace = True, p= scores)
	guess = input('Enter your first guess, then press ENTER. I suggest the word {}. '.format(suggestion))
	#3. output the response array of colors
	response = words.compare(guess, solution)
	print('Here are the results from your guess: \n', response[0], response[1],response[2],response[3], response[4])
	# words_list is modified to only include possible words
	words_list,frequencies = words.sort(words_list, frequencies, guess, response)	

	return guess, words_list,frequencies

def guess2(solution,guess1,words_list, frequencies):
	'''
		Function to run the code for the user's second guess 

		Parameters
		----------
		solution
			of the wordle run
		response
			response from guess 1
		words_list
			the possible words remaining after guess1
		scores
			scores given to each word
		frequencies
			frequencies of each word in the english language
		scores_ordered_indices 
			the ordered indices of the words with respect to their score (descending)

		Returns
		----------
		guess
			the guess
		words_list
			the list of all words that can still be the answer
		frequencies
			their frequencies
	'''
	#2. asks the user for a first guess and provide a suggestion of the best option (based on difference score = we want to suggest a word with different letters from the first guess)
	difference_score = proba.compute_difference_score(words_list,guess1) 
	indices = [i for i, x in enumerate(difference_score) if x == 5]
	new_frequencies = np.take(frequencies,indices)
	new_words_list = np.take(words_list,indices)
	new_frequencies = new_frequencies/sum(new_frequencies)
	suggestion = np.random.choice(new_words_list,size = None, replace = True,p=new_frequencies)
	#normalize the frequencies and scores so that they sum to 1 and hence can be used as probabilities
	guess = input('Guess again and press ENTER. I suggest the word {}. '.format(suggestion))
	#3. output the response array of colors
	response = words.compare(guess, solution)
	print('Here are the results from your guess: \n', response[0], response[1],response[2],response[3], response[4])
	# words_list is modified to only include possible words
	words_list,frequencies = words.sort(words_list, frequencies, guess, response)	

	return guess, words_list,frequencies

		
