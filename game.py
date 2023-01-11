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

#to print the full lengh of arrays
import sys
np.set_printoptions(threshold=sys.maxsize)

# @profile
def initialize():
	'''
		Function that initiliazes the game, meaning it runs everything until the first interaction with the user

		Parameters
		----------

		Returns
		----------
		interactive
			bool corresponding to the player's choice to play the interactive version or not
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word based on letter frequencies (in words and in a particular place in the word)
		frequencies
			frequencies of each word in the english language
	'''
	answer = input('Welcome to the Wordle Solver, would you like to play interactively or ask me to solve for a word? Write INTERACT or SOLVE and press ENTER: ')
	#make sure only accepted answers are given, run the loop until the answer is valid
	is_correct = False
	while not is_correct:
		if answer.lower() == 'interact':
			interactive = True
			is_correct = True
		elif answer.lower() == 'solve':
			interactive = False
			is_correct = True
		else:
			answer = input('Invalid answer, please try again: ')


	#load of all the words into a list
	words_list = words.load_list()

	#compute the arrays containing the scores and frequencies of each word in the list
	scores, frequencies = proba.compute_all(words_list)

	#normalize the frequencies and scores so that they sum to 1 and hence can be used as probabilities
	frequencies = proba.renormalize(frequencies)
	scores = proba.renormalize(scores)


	return interactive, words_list, scores, frequencies
# @profile

def pick_solution(words_list,interactive):
	'''
		Function that picks the solution word based on which version the user wants to play 

		Parameters
		----------
		words_list
			array, the list of all words accepted by Wordle
		interactive
			boolean, True if interactive, false if solve

		Returns
		----------
		solution
			string, the word chosen as the solution to the round of Wordle
	'''
	#word chosen randomly from the words_list or chosen by the user
	if interactive:
		solution = np.random.choice(words_list,size = None, replace = True)
	else:
		solution = input('Type in the 5 letter word you would like me to guess (I wont peek!!), then press ENTER: ')
		solution = (words.verify(solution)).lower() #always lower strings to make sure there is no capitalization error
	return solution

def guess_run(words_list, solution, probability_distribution,interactive):
	'''
		Function that makes the computer guess until the solution given by the user is found

		Parameters
		----------
		words_list
			array, the list of all words accepted by Wordle
		probability_distribution
			array of the chosen probability distribution for the list of possible words
		interactive
			boolean, True if interactive, false if solve
		Returns
		----------
		tries
			int, the number of guesses until finding the right one
	'''
	tries = 1
	solution_found = False

	guess1, words_list_1,probability_distribution1 = try_guess(solution, words_list, probability_distribution,interactive) 
	
	tries +=1
	guess2, words_list_2,probability_distribution2 = try_guess(solution,words_list,probability_distribution, interactive, previous_guess = guess1)
	#the words_list used is the intersection of the two resulting from the first two guesses
	words_list,indices1,indices2 = np.intersect1d(words_list_1,words_list_2,assume_unique=False, return_indices=True)
	probability_distribution = np.take(probability_distribution1, indices1)
	#renormalize
	probability_distribution = proba.renormalize(probability_distribution)

	#loop until the right word is found
	while not solution_found:
		tries+= 1
		guess, words_list, probability_distribution  = try_guess(solution, words_list, probability_distribution, interactive)

		if guess == solution:
			solution_found = True

	return tries, solution
# @profile
def try_guess(solution, words_list, probability_distribution, interactive, previous_guess = None):
	'''
		Function to make the user/computer guess

		Parameters
		----------
		solution
			string, solution of the wordle run
		words_list
			array, the list of all words accepted by Wordle
		probability_distribution
			array of the chosen probability distribution for the list of possible words
		interactive
			boolean, True if interactive, false if solve
		previous_guess
			string, previous guess (needed if we are at guess 2)

		Returns
		----------
		guess
			string, the guess
		words_list
			array, the list of all words that can still be the answer
		probability_distribution
			array of the chosen probability distribution for the list of possible words
	'''

	#generate the suggestion depending on the number of the guess
	suggestion = generate_guess(words_list, probability_distribution, interactive, previous_guess)
	#obtain/generate the guess depending on the chosen mode 
	if interactive:
		#give the option to see the full list of possible words at this stage
		guess = input('Enter your guess, then press ENTER. I suggest the word {}. If you want more suggestions, enter MORE. ' .format(suggestion))
		if guess.lower() == 'more':
			words.print_list(words_list)
			guess = input('Now enter your guess. Reminder: I suggest the word {}. ' .format(suggestion))
			guess = (words.verify(guess)).lower() 
		else:
			guess = (words.verify(guess)).lower() 
	else:
		guess = suggestion
		print('I am guessing the word {}. '.format(suggestion))

	#exit the function if the guess matches the solution
	if guess.lower() == solution:
		return guess, None, None
	
	#compute the response array of colors
	response = words.compare(guess, solution)
	print('Here are the results: \n', response[0], response[1],response[2],response[3], response[4])

	# words_list is modified to only include possible words, and the frequency array is modified accordingly
	words_list,probability_distribution = words.sort(words_list, probability_distribution, guess, response)

	probability_distribution = proba.renormalize(probability_distribution)

	return guess, words_list, probability_distribution	

def generate_guess(words_list, probability_distribution, interactive, previous_guess = None):
	'''
		Function to generate the guess/suggestion

		Parameters
		----------
		words_list
			the list of all words accepted by Wordle
		probability_distribution
			array of the chosen probability distribution for the list of possible words
		interactive
			True if interactive, false if solve
		previous_guess
			previous guess (needed for second guess) or None if any other guess

		Returns
		----------
		suggestion
			string, for the next guess
	'''
	if previous_guess == None:
		suggestion = np.random.choice(words_list,size = None, replace = True, p= probability_distribution)
	else:
		difference_score = proba.compute_difference_score(words_list,previous_guess) 
		#only select from words that have all different letters than guess 1
		indices = [i for i, x in enumerate(difference_score) if x == 5] 
		new_frequencies = np.take(probability_distribution,indices)
		new_words_list = np.take(words_list,indices) #containing only the words with a score of 5
		new_frequencies = new_frequencies/sum(new_frequencies)
		suggestion = np.random.choice(new_words_list,size = None, replace = True,p=new_frequencies)		
		
	return suggestion
