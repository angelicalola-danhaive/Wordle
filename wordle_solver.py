"""
Full code to run to solve WORDLE yourself interactively or to give the program a word and get it to solve it
	Written by A L Danhaive: ald66@cam.ac.uk
"""
#load all of the modules 
import numpy as np
import game

#initialize the game: ask if the payer wants to play interactively or in bash, load the wordlewords.txt file, compute all probabilities and store them somewhere

interactive, words_list, scores, frequencies = game.initialize()
probability_distribution = scores
solution = game.pick_solution(words_list, interactive)
tries, solution = game.guess_run(words_list, solution, probability_distribution,interactive)
print('Congrats! You found the correct word, {}, in {} tries. '.format(solution, tries))