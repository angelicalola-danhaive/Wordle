"""
This is a code to solve WORDLE.

This code allows you to do the following:

1. Solve for any 5-letter word in the WordleWords.txt, with the ENTER + 'solve' option
2. Play Wordle yourself by choosing the interactive option, with the ENTER + 'interactive' option
3. Run the solver over all of the words in WordleWords.txt to compute the average amount of guesses it takes to solve a word, with the 'run' option

It generates guesses based on the frequencies of letters in order to optimize the information gotten from each guess.

	Written by A L Danhaive: ald66@cam.ac.uk
"""

#load all of the modules 
import numpy as np
import game
import words
import random


ask_user = input('If you would like to run the code on the full list of words, enter RUN. If not, just press ENTER. ')

if ask_user.lower() == 'run':
	#--------------run it automatically on a set of words --------------------------------------------------------------------------------------------

	#initialize arrays that will contain the number of guesses for each word
	words_list = words.load_list()
	tries_total = np.zeros(len(words_list))

	#initalize the game to batch automatically
	interactive, new_words_list, scores = game.initialize(True)

	#make it solve for every word in the list
	for index,word in enumerate(words_list):
		solution = word
		tries= game.guess_run(new_words_list, solution, scores,interactive)
		tries_total[index] = tries
		print('Just finished word number {}'.format(index+1) )

	#to plot the results from the run of the list
	import matplotlib.pyplot as plt
	#number_tries will be the bins, and the height is given by how many time that number appears in the array of the number of tries for each word
	number_tries, height_tries = np.unique(tries_total, return_counts = True)
	#compute and print the mean number of tries
	mean = np.mean(tries_total)
	print('The average number of tries is: {} '.format(mean))

	#plot the histogram
	plt.bar(number_tries, height_tries) 
	plt.show()


else:
	#---------------run just once-------------------------------------------------------------------------------------------------------------------


	# initialize the game: ask if the payer wants to play interactively or in batch, load the wordlewords.txt file, compute all probabilities and store them somewhere

	#load the list of words and their scores, and ask the user to set the interactive bool 
	interactive, words_list, scores = game.initialize()
	#generate the solution for the round
	solution = game.pick_solution(words_list, interactive)
	#run the game until the solution is found
	tries = game.guess_run(words_list, solution, scores,interactive)
	print('The correct word, {}, was found in {} tries. '.format(solution, tries))

