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

# @profile
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
	correct = False
	while not correct:
		if answer.lower() == 'interact':
			interactive = True
			correct = True
		elif answer.lower() == 'solve':
			interactive = False
			correct = True
		else:
			answer = input('Invalid answer, please try again: ')


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
# @profile
def guess_run(words_list, scores, frequencies,interactive):
	'''
		Function that makes the computer guess until the solution given by the user is found

		Parameters
		----------
		words_list
			the list of all words accepted by Wordle
		scores
			scores given to each word
		frequencies
			frequencies of each word in the english language
		interactive
			True if interactive, false if solve
		Returns
		----------
		tries
			the number of guesses until finding the right one
	'''
	tries = 1
	solution_found = False
	#1. the user is asked to give a five letter word
	if interactive:
		solution = np.random.choice(words_list,size = None, replace = True, p= frequencies)
	else:
		solution = input('Type in the 5 letter word you would like me to guess (I wont peek!!), then press ENTER: ')
		solution = (words.verify(solution)).lower() #always do the word check with the full list

	guess1, words_list_1,frequencies_1 = try_guess(solution, words_list, frequencies, interactive, scores, 1) 
	
	tries +=1
	guess2, words_list_2,frequencies_2 = try_guess(solution,words_list,frequencies, interactive, number = 2, previous_guess = guess1)
	#the words_list used is the intersection of the two resulting from the first two guesses
	words_list,indices1,indices2 = np.intersect1d(words_list_1,words_list_2,assume_unique=False, return_indices=True)
	frequencies = np.take(frequencies_1, indices1)
	#renormalize
	frequencies = frequencies/frequencies.sum()

	#loop until the right word is found
	while not solution_found:
		tries+= 1
		guess, words_list, frequencies  = try_guess(solution, words_list, frequencies, interactive)

		if guess == solution:
			solution_found = True

	return tries, solution
# @profile
def try_guess(solution, words_list, frequencies, interactive, scores = None, number = 0, previous_guess = None):
	'''
		Function to make the user/computer guess

		Parameters
		----------
		solution
			of the wordle run
		words_list
			the list of all words accepted by Wordle
		frequencies
			frequencies of each word in the english language
		interactive
			True if interactive, false if solve
		scores
			scores given to each word (needed if we are at guess 1)
		number
			1 for first guess, 2 for second guess, 0 for all of the others. This determines the method to chose the next suggestion
		previous_guess
			previous guess (needed if we are at guess 2)

		Returns
		----------
		guess
			the guess
		words_list
			the list of all words that can still be the answer
		frequencies
			their frequencies
	'''
	#generate the suggestion depending on the number of the guess
	if number == 1:
		suggestion = np.random.choice(words_list,size = None, replace = True, p= scores)	
	elif number == 2:
		difference_score = proba.compute_difference_score(words_list,previous_guess) 
		#only select from words that have all different letters than guess 1
		indices = [i for i, x in enumerate(difference_score) if x == 5] 
		new_frequencies = np.take(frequencies,indices)
		new_words_list = np.take(words_list,indices) #containing only the words with a score of 5
		new_frequencies = new_frequencies/sum(new_frequencies)
		suggestion = np.random.choice(new_words_list,size = None, replace = True,p=new_frequencies)
	else:
		suggestion = np.random.choice(words_list,size = None, replace = True, p= frequencies)
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

	#3. output the response array of colors
	response = words.compare(guess, solution)
	print('Here are the results: \n', response[0], response[1],response[2],response[3], response[4])
	# words_list is modified to only include possible words
	words_list,frequencies = words.sort(words_list, frequencies, guess, response)	
	frequencies = np.array(frequencies)/sum(frequencies)

	return guess, words_list,frequencies	


		
