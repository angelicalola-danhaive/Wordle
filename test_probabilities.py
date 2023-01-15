"""
	This Module contains the unit tests for the functions in  probabilities.py
	
	Contains:
	----------------------------------------
	test_compute_all
		test for the compute_all function
	test_compute_letter_frequencies 
		test for the compute_letter_frequencies function
	test_compute_difference_score
		test for the compute_difference_score function
	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
	"""

import probabilities
import numpy as np

def test_compute_all():
	"""
		Test for the compute_scores function
	"""

	assert(np.all((probabilities.compute_all(['woman'])) == [10/10]))
	assert(np.all((probabilities.compute_all(['wasps'])) == [12/(10*2)]))
	assert(np.all(probabilities.compute_all(['wasps'], True) == [0]))

def test_compute_letter_frequencies():
	"""
		Test for the compute_letter_frequencies function
	"""

	assert(np.all(probabilities.compute_letter_frequencies(['abcdc','adbec']) == [ [2,2,0,0,0,0], [2,0,1,1,0,0], [3,0,0,1,0,2] ,[2,0,1,0,1,0], [1,0,0,0,1,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ]))


def test_compute_difference_score():
	"""
		Test for the compute_difference_score function
	"""
	assert( np.all( probabilities.compute_difference_score(['right','wrong'], 'wrong') == [3,0] )  ) 