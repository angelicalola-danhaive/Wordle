"""
	This Module contains the unit tests for the functions in  words.py
	
	Contains:
	----------------------------------------
	test_compare
		Test for the compare function
	test_sort
		Test for the sort function
	test_check_word
		Test for the check_word function
	test_count_difference
		Test for the count_difference function
	test_verify
		Test for the verify function
	test_load_list
		Test for the load_list function
	----------------------------------------
	
	
	Written by A L Danhaive: ald66@cam.ac.uk
	"""

import words
import numpy as np
import pandas

from unittest import mock

def test_compare():
	"""
	Test for the compare function
	"""
	#checks that need to be done: letter is in the right spot, letter is in the wrong spot, double letter in guess one in solution, vice versa

	assert(words.compare('table','tower') == ['G', 'B', 'B', 'B', 'Y' ])
	assert(words.compare('books','sport') == ['B', 'B', 'G', 'B', 'Y' ])
	assert(words.compare('sport','books') == ['Y', 'B', 'G', 'B', 'B' ])
	assert(words.compare('spook', 'troon') == ['B', 'B', 'G', 'G', 'B' ])
	assert(words.compare('sopok', 'troon') == ['B', 'Y', 'B', 'G', 'B' ])
	assert(words.compare('goofy', 'oxbow') == ['B', 'Y', 'Y', 'B', 'B' ])

def test_sort():
	"""
	Test for the sort function
	"""
	#checks: general, all black, all green, all yellow word
	#in all the checks we assume the right word is wagon (for the response array)
	assert(np.all((words.sort(['above','wasps','zebra', 'wagon'], 'weary', ['G','B','Y','B','B'])) == ['wasps', 'wagon']))
	assert(np.all((words.sort(['above','wasps','zebra', 'wagon'] ,'plith', ['B','B','B','B','B'])) == ['above','zebra', 'wagon']))
	assert(np.all((words.sort(['above','wasps','zebra', 'wagon'],  'wagor', ['G','G','G','G','B'])) == ['wagon']))
	assert(np.all((words.sort(['above','wasps','zebra', 'wagon'], 'noawg', ['Y','Y','Y','Y','Y']))== ['wagon']))

def test_check_word():
	"""
	Test for the check_word function
	"""
	assert(words.check_word('aliuf',['a'],[0], ['i'] , [3] , ['g','a','n'] ) == True)
	assert(words.check_word('sixes',['s', 'i', 'e' ,'s'],[0,1,3,4], [] , [] , ['s'] ) == True)
	# assert(words.check_word(list('wasps'),list('wagon'),['G', 'Y', 'B', 'B','B'] ) == False)
	# assert(words.check_word(list('sixes'),list('sises'),['G', 'G', 'B', 'G','G'] ) == True)


def test_count_difference():
	"""
	Test for the count_difference function
	"""
	assert(words.count_difference('wagon','wasps') == 3)

def test_verify():
	"""
	Test for the verify function
	"""
	assert(  words.verify('zebra') == 'zebra' )
	#check that if the wrong word is put then it requests another
	with mock.patch('builtins.input', return_value="zebra"):
		assert(  words.verify('ablar') == 'zebra' )

def test_load_list():
	"""
	Test for the load_list function
	"""
	words_list = words.load_list()
	#check that all of the words have been loaded
	assert(len(words_list) == 12947) 
	#check that none of the slots are empty
	assert( pandas.isnull( words_list ) .any() == False)

