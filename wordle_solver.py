"""
Full code to run to solve WORDLE yourself interactively or to give the program a word and get it to solve it
	Written by A L Danhaive: ald66@cam.ac.uk
"""
#load all of the modules 
import numpy as np
import words
import game

#initialize the game: ask if the payer wants to play interactively or in bash, load the wordlewords.txt file, compute all probabilities and store them somewhere

interactive, words_list, scores, frequencies, scores_ordered_indices = game.initialize()

if interactive: 
	# in the interactive version: 
	tries, solution = game.guess_interactive(words_list, scores, frequencies, scores_ordered_indices)
	print('Congrats! You found the correct word, {}, in {} tries. '.format(solution, tries))


# else:
	#in the bash version:
	#1. the user inputs a word (check that it is in the list)
	#2. print the first guess and the resulting reponse array
	#4. => same function as interactive, never ask for input but just display the work that it is doing