"""
Full code to run to solve WORDLE yourself interactively or to give the program a word and get it to solve it
	Written by A L Danhaive: ald66@cam.ac.uk
"""
#load all of the modules 
import numpy as np
import initialize as init
import words

#initialize the game: ask if the payer wants to play interactively or in bash, load the wordlewords.txt file, compute all probabilities and store them somewhere
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
scores, frequencies = init.compute_all(words_list)

#normalize the frequencies so that they sum to 1 and hence can be used as probabilities
frequencies = frequencies/frequencies.sum()

#sort the indices of the words in order from highest to lowest score/frequency (have to flip because function gives them in ascending order and we want descending for simplicity)
scores_ordered_indices = np.flip(np.argsort(scores))

frequencies_ordered_indices =  np.flip(np.argsort(frequencies))

if True: 
	# in the interactive version: 
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
	print(words_list, frequencies)
	#4. based on that, ask for another guess and provide a suggestion (based on most common words)
	suggestion = words_list[np.argmax(frequencies)]
	guess = input('Guess again and press ENTER. I suggest the word {}. '.format(suggestion))
	#5. this is looped until the user has found the right answer => put this all into a function!


# else:
	#in the bash version:
	#1. the user inputs a word (check that it is in the list)
	#2. print the first guess and the resulting reponse array
	#4. => same function as interactive, never ask for input but just display the work that it is doing