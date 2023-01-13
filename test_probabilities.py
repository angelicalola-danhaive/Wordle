"""
	This Module contains the unit tests for the functions in  probabilities.py
	
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
	"""

import probabilities
import numpy as np

def test_compute_letter_frequencies():
	"""
		Test for the compute_letter_frequencies function
	"""

	assert(np.all(probabilities.compute_letter_frequencies(['bubby', 'buchu']) == [0., 4, 1, 0., 0., 0., 0., 1, 0, 0. ,0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 3, 0., 0., 0., 1, 0.] ) )

def test_compute_all():
	"""
		Test for the compute_scores function
	"""

	assert(np.all((probabilities.compute_all(['woman'])) == [5]))
	assert(np.all((probabilities.compute_all(['wasps'])) == [7]))
	assert(np.all(probabilities.compute_all(['wasps'], True) == [0]))

def test_renormalize():
	"""
		Test for the renormalize function
	"""
	assert( np.all(probabilities.renormalize( [5,5] ) == [0.5,0.5]) )
	assert( np.all(probabilities.renormalize( [0.0,0.0] ) == [1])  )

def test_compute_difference_score():
	"""
		Test for the compute_difference_score function
	"""
	assert( np.all( probabilities.compute_difference_score(['right','wrong'], 'wrong') == [3,0] )  ) 