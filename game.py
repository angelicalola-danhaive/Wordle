"""
	This Module contains functions needed to interact with the user and play the game.
	Contains:
	----------------------------------------
	initialize
		initializes the game
	pick_solution 
		generates the solution for the round based on the user's choice of game mode
	guess_run
		the main function of the game, iterating over guesses until the solution is found
	try_guess
		function to compare a guess with the solution and output the response
	generate_guess
		generates a guess based on which guess it is (first, second, or other)
	----------------------------------------
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""

#imports 
import words
import probabilities as proba
import numpy as np

#import needed to print the full lengh of arrays - for testing purposes
import sys
np.set_printoptions(threshold=sys.maxsize)


def initialize(run_in_bash = False):
	'''
		Function that initiliazes the game, running everything until the first interaction with the user

		Parameters
		----------
		run_in_bash
			boolean, True if the user wants to run the code in bash looping over a list of words
		Returns
		----------
		interactive
			boolean corresponding to the player's choice to play the interactive version or not
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word based on letter frequencies (in words and in a particular place in the word)
	'''

	#directly set interactive to false so that the code can run without user inputs
	if run_in_bash:
		interactive = False 
	else:
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

	#compute the arrays containing the scores  of each word in the list
	scores= proba.compute_all(words_list,True)


	return interactive, words_list, scores

def pick_solution(words_list,interactive):
	'''
		Function that picks the solution word based on which version the user wants to play 

		Parameters
		----------
		words_list
			array, the list of all words accepted by Wordle
		interactive
			boolean, True if interactive, false if solving in bash

		Returns
		----------
		solution
			string, the word chosen as the solution to the round of Wordle
	'''
	#word chosen randomly from the words_list or chosen by the user. If chosen by the user, make sure the word is in the list of possible words
	if interactive:
		solution = np.random.choice(words_list,size = None, replace = True)
	else:
		solution = input('Type in the 5 letter word you would like me to guess (I wont peek!!), then press ENTER: ')
		solution = (words.verify(solution)).lower() #always lower strings to make sure there is no capitalization error
	return solution

def guess_run(words_list, solution, scores,interactive):
	'''
		Function to keep guessing until the solution is found

		Parameters
		----------
		words_list
			array, the list of all words accepted by Wordle
		solution
			string, word to be solved for
		scores
			scores given to each word based on letter frequencies (in words and in a particular place in the word)
		interactive
			boolean, True if interactive, false if solve
		Returns
		----------
		tries
			int, the number of guesses until finding the right one
	'''
	#initialize the tries to one since at least one guess is mandatory
	tries = 1
	#initilize boolean to False, will be set to True when the solution is found
	solution_found = False

	#for the first 2 guesses, guess 2 words with fully different letters and then combine the results from both responses

	guess1, words_list_1,scores1 = try_guess(solution, words_list, scores,interactive) 

	if guess1==solution:
		return tries, solution
	
	tries +=1
	guess2, words_list_2,scores2 = try_guess(solution,words_list,scores, interactive, guess1)

	if guess2==solution:
		return tries, solution

	#the words_list used is the intersection of the two resulting from the first two guesses
	words_list = np.intersect1d(words_list_1,words_list_2,assume_unique=False)

	#recompute the scores for the words in this new list
	scores = proba.compute_all(words_list)

	#loop over guesses until the right word is found
	while not solution_found:
		tries+= 1
		guess, words_list, scores  = try_guess(solution, words_list, scores, interactive)

		if guess == solution:
			solution_found = True
	return tries


def try_guess(solution, words_list, scores, interactive, previous_guess = None):
	'''
		Function to make the user/computer guess

		Parameters
		----------
		solution
			string, solution of the wordle run
		words_list
			array, the list of all words accepted by Wordle
		scores
			scores given to each word based on letter frequencies (in words and in a particular place in the word)
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
		scores
			scores given to each word in the new list
	'''

	#generate the suggestion depending on the number of the guess
	suggestion = generate_guess(words_list, scores, interactive, previous_guess)

	#obtain/generate the guess depending on the chosen mode. if interactive, the user is free to choose his own guess
	if interactive:
		#give the option to see the full list of possible words at this stage
		guess = input('Enter your guess, then press ENTER. I suggest the word {}. If you want more suggestions, enter MORE. ' .format(suggestion))
		if guess.lower() == 'more':
			words.print_list(words_list)
			guess = input('Now enter your guess. Reminder: I suggest the word {}. ' .format(suggestion))
			guess = (words.verify(guess)).lower() 
		else:
			guess = (words.verify(guess)).lower() 

	#if run in bash, then the computer uses the suggestion as the guess and displays it to the user
	else:
		guess = suggestion
		print('I am guessing the word {}. '.format(suggestion))

	#exit the function directly if the guess matches the solution
	if guess.lower() == solution:
		return guess, None, None
	
	#compute and display the response array of colors 
	response = words.compare(guess, solution)
	print('Here are the results: \n', response[0], response[1],response[2],response[3], response[4])

	# words_list is modified to only include possible words, and the scores array is recomputed for those words
	words_list= words.sort(words_list, guess, response)
	scores = proba.compute_all(words_list)

	return guess, words_list, scores	

def generate_guess(words_list, scores, interactive, previous_guess = None):
	'''
		Function to generate the next guess/suggestion

		Parameters
		----------
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word in the new list
		interactive
			True if interactive, false if solve
		previous_guess
			previous guess (needed for second guess) or None if any other guess

		Returns
		----------
		suggestion
			string, suggestion for the next guess
	'''
	#if not the second guess, then the suggestion is the word with the highest score
	if previous_guess == None:
		suggestion = words_list[np.argmax(scores)]
	#for the second guess, the word is still chosen based on the highest score but is only selected from a narrowed-down list of words with fully different letters from the previous guess
	else:
		difference_score = proba.compute_difference_score(words_list,previous_guess) 
		#only select from words that have all different letters than guess 1
		indices = [i for i, x in enumerate(difference_score) if x == 5] 
		new_words_list = np.take(words_list,indices) #containing only the words with a score of 5
		new_scores = np.take(scores,indices)
		suggestion = new_words_list[np.argmax(new_scores)]	
		
	return suggestion
