"""
	This Module contains the unit tests for the functions in  initialize.py
	
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

	assert(np.all(probabilities.compute_letter_frequencies(['abcdc','adbec']) == [ [2,2,0,0,0,0], [2,0,1,1,0,0], [3,0,0,1,0,2] ,[2,0,1,0,1,0], [1,0,0,0,1,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ]))

def test_compute_all():
	"""
		Test for the compute_scores function
	"""

	assert(np.all((probabilities.compute_all(['woman']))[0] == [10]))
	assert(np.all((probabilities.compute_all(['woman']))[1] == [5.35]))
	assert(np.all((probabilities.compute_all(['eases']))[0] == [0]))
	assert(np.all((probabilities.compute_all(['eases']))[1] == [2.93]))

def test_compute_difference_score():
	assert(np.all(probabilities.compute_difference_score(['wagon','early'],'wasps') == [3,4]   ))