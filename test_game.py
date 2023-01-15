"""
	This Module contains the unit tests for the functions in  game.py
	
	Contains:
	----------------------------------------
	test_initialize
		test for the initialize function
	test_try_guess
		test for the try_guess function
	test_generate_guess
		test for the generate_guess function
	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
	"""

#general imports
from unittest import mock #to give an input so that the test can run
import numpy
import pandas

#imports from our modules
import game
import words
import probabilities as proba

#generate the list and its scores so that the functions can be tested on the full list
words_list = words.load_list()
scores = proba.compute_all(words_list)


def test_initialize():
	"""
		Test for the initialize function
	"""
	with mock.patch('builtins.input', return_value="solve"):

		interactive, words_list, scores = game.initialize()
		#check that the interactive variable is indeed a Boolean
		assert(type(interactive) == type(True) )
		#check that there are as many elements in scores/frequency arrays as in the words_list
		assert( len(words_list) == len(scores) )
		#check that none of the elements in each are zero or 
		#pandas is needed for type strings
		assert( pandas.isnull( words_list ) .any() == False)
		assert( numpy.isnan(scores).any() == False)

def test_try_guess():
	"""
		Test for the try_guess function
	"""

	guess, new_words_list, new_scores = game.try_guess('woman', words_list, scores,False )

	#check that there are as many elements in scores/frequency arrays as in the words_list
	assert( len(new_words_list) == len(new_scores) )
	#check that none of the elements are NaN
	assert( numpy.isnan(new_scores).any() == False )
	assert( pandas.isnull( words_list ) .any() == False)

def test_generate_guess():
	"""
		Test for the try_guess function
	"""
	#test that the second guess has fully different letters
	suggestion = game.generate_guess(words_list, scores, 'wagon')
	same = (set(suggestion)&set('wagon'))

	assert(len(same) == 0)

