"""
	This Module contains functions to use and compare words.
	
	Contains:
	----------------------------------------
	compare
		compares the guess and solution and outputs the corresponding response array
	sort
		sorts the words_list to only include words that are compatible with the response array from the previous guess
	check_word
		compares a word with the response array and outputs a True if the word is still possible and False otherwise
	count_difference
		counts the number of characters that differ between two words
	verify
		function that verifies if a word is in the list of accepted words and loops until a correct one is given
	load_list
		load the list of words from the WordleWords.txt file
	print_list
		print all of the words in a give words_list
	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
"""

#imports
import numpy as np

def compare(guess,solution):
	"""
		Comparing the characters of the guess and solution to output the color indicators
		
		Parameters
		----------
		guess
			the guess offered by the user
		solution
			the answer to be compared to the guess

		Returns
		----------
		response
			the array of colors corresponding to how correct the letters in the guess are
			the colors are 'B' for black (letter not in word), 'Y' for yellow (letter in word but wrong place), 'G' for green (letter in the right place)
	"""
	#initalize response as all black by default and modify entries that are green or yellow
	response = list(['B','B','B','B','B'])

	#turn the array into a list so that it's easier for operations
	guess_array = list(guess)
	solution_array = list(solution)

	#element wise comparison with np.compare_chararrays() => outputs a bool array with True if the right letter is in the right place
	green_letters = np.char.compare_chararrays(guess_array, solution_array,'==',rstrip = True )

	# add the green letters in the response and then 'delete' them from the words so that the search for yellow letters (especially for double letters) doesn't consider the green ones
	for i,letter in enumerate(green_letters):
		if letter:
			response[i] = 'G'
			guess_array[i] = '*'
			solution_array[i] = '#'

	#select yellow letters by seeing if there is still an overlap between guess and solution after removing the green ones
	#again, letters are replaced when checked so that double letters can be taken into account without overlap
	for index,letter in enumerate(guess_array):
		if letter in solution_array:
			response[index]= 'Y'
			guess_array[index] = '*'
			#to get the index of the first occurence of the letter in the solution array
			characters, index_in_solution, index_in_letter = np.intersect1d(solution_array, letter, return_indices = True)
			index_in_solution = index_in_solution[0] #take the first (and only) element because index_in_solution is an array, and we want an int
			solution_array[index_in_solution] = '#' 

	#any letters that aren't green or yellow remain black
	return response


def sort(words_list,guess,response):
	"""
		Sort through the words_list to only keep words that match the response array
		
		Parameters
		----------
		words_list
			the list of possible words for the previous guess
		guess
			the guess offered by the user
		reponse
			array with the colors corresponding to the guess

		Returns
		----------
		words_list
			the updated list of possible words
	"""

	#initialize all of the arrays that will be filled within the function
	new_list = []

	green_letters = []
	green_indices = []

	yellow_letters = []
	yellow_indices = []

	black_letters = []

	#sort through the letters to make the sorting through the words easier
	for index,letter in enumerate(guess):
		if response[index] == 'G':
			green_letters.append(letter)
			green_indices.append(index)
		if response[index] == 'Y':
			yellow_letters.append(letter)
			yellow_indices.append(index)
		if response[index] == 'B':
			black_letters.append(letter)

	#check which words have all the greens in right spot, have the yellows NOT in the same spot as the guess but still in the word, and don't have blacks
	for index,word in enumerate(words_list):
		keep = check_word(list(word), green_letters,green_indices, yellow_letters, yellow_indices, black_letters)
		if keep: 
			new_list.append(word)
	return new_list

def check_word(word,green_letters,green_indices, yellow_letters, yellow_indices, black_letters):
	'''
		Checking if a word matches the response array obtained from the guess

		Parameters
		----------
		word
			word that we want to test, array
		green_letters, green_indices
			arrays with the green letters and their place in the word
		yellow_letters, yellow_indices
			arrays with the yellow letters and their place in the word
		black_letters
			array with the black letters

		Returns
		----------
		bool
			a boolean indicating if the word matches the reponse (True) or doesn't and should hence be removed from the list (False)
	'''	

	#check if the word has all of the green letters in the right spot 
	if len(green_letters)!= 0:
		for i in range(len(green_letters)):
			if word[green_indices[i]] != green_letters[i]:
				return False

	#check if the word has the yellow letters NOT in the same spot as the guess but still in the word
	if len(yellow_letters)!= 0:
		for i in range(len(yellow_letters)):
			if word[yellow_indices[i]] == yellow_letters[i] or (yellow_letters[i] not in word):
				return False		

	#check if the word doesn't have black letters
	if len(black_letters)!= 0:
		for i in range(len(black_letters)):
			#account for double/triple letters: if the black letter is also in another set, then it is allowed to be in the word but only a certain amount of times
			if ( (black_letters[i] in green_letters) or (black_letters[i] in yellow_letters) ):
			#only discard a word if it has the black letter too many times
				if word.count(black_letters[i])> ( green_letters.count(black_letters[i]) + yellow_letters.count(black_letters[i]) ): 
					return False
				else:
					return True
			#if its not in the other sets then its not allowed to be in the word at all
			elif black_letters[i] in word :
				return False

	#if all checks have passed then return True 
	return True	


def count_difference(guess2, guess1):
	'''
		Counting how many letters differ between two words

		Parameters
		----------
		guess1
		guess2
			the two words we want to compare. guess 1 is the previous guess and guess2 is the word being tested to be guessed next

		Returns
		----------
		different
			int of the number of letters differring between word1 and word2
	'''

	#the & operator between two sets computes their intersection
	same =set(guess1)&set(guess2)
	#return the difference = total - same
	return 5-len(same)


def verify(word):
	'''
		Check that the word given as input is a valid wordle word

		Parameters
		----------
		word
			string, input that you want to verify is in the list of accepted words
		Returns
		----------
		word
			word that has been checked
	'''
	#compute the words list
	words_list = load_list()
	#check if input is in that list, if not request a new one until a valid one is given
	correct = False
	while not correct:
		if word.lower() not in words_list:
			word = input('Error: Invalid word! Please provide another 5 letter word: ')
		else: 
			return word

def load_list():
	'''
		Load the possible Wordle words from the WordleWords.txt file into an array 

		Parameters
		----------
		
		Returns
		----------
		words_list
			array of all possible Wordle words
	'''
	with open('WordleWords.txt') as file:
		words_list = [line.rstrip() for line in file] 
	return words_list


def print_list(words_list):
	'''
		Print all of the words from a given list

		Parameters
		----------
		words_list
			list of words too be printed
		Returns
		----------
	'''
	for word in words_list:
		print(word)

	return None