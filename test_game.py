"""
	This Module contains the unit tests for the functions in  gamee.py
	
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
	"""
from unittest import mock
import numpy
import pandas

import game

def test_initialize():
	"""
		Test for the initialize function
	"""
	with mock.patch('builtins.input', return_value="solve"):

		#check that the interactive variable is indeed a Boolean
		assert(type((game.initialize())[0]) == type(True) )
		#check that there are as many elements in scores/frequency arrays as in the words_list
		assert( len((game.initialize())[1]) == len((game.initialize())[2]) )
		#check that none of the elements in each are zero or 
		#pandas is needed for tyoe strings
		assert( pandas.isnull( (game.initialize())[1] ) .any() == False)
		assert( numpy.isnan((game.initialize())[2]).any() == False)
		#np.all() return True if there are no zeros, and False if there is at least one zero 
		#for now only check scores until I decide if to keep frequencies or not
		# assert( numpy.all((game.initialize())[2]) == True)
