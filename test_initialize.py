"""
	This Module contains the unit tests for the functions in  initialize.py
	
	Contains:
	----------------------------------------

	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
	"""

import initialize
import numpy as np

def test_compute_letter_frequencies():
	"""
		Test for the compute_letter_frequencies function
	"""

	assert(np.all(initialize.compute_letter_frequencies(['abcdc','adbec']) == [ [2,2,0,0,0,0], [2,0,1,1,0,0], [3,0,0,1,0,2] ,[2,0,1,0,1,0], [1,0,0,0,1,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ,[0,0,0,0,0,0], [0,0,0,0,0,0] ,[0,0,0,0,0,0] ]))

def test_compute_scores():
	"""
		Test for the compute_scores function
	"""

	assert(np.all(initialize.compute_scores(['abcdc','adbec']) == [19,17]))