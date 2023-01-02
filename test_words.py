"""
    This Module contains the unit tests for the functions in  words.py
    
    Contains:
    ----------------------------------------

    ----------------------------------------
    
    
    Written by A L Danhaive: ald66@cam.ac.uk
    """

import words
import numpy as np

def test_compare():
    """
    Test for the compare function
    """
    #checks that need to be done: letter is in the right spot, letter is in the wrong spot, double letter in guess one in solution, vice versa

    assert(words.compare('table','tower') == ['G', 'B', 'B', 'B', 'Y' ])
    assert(words.compare('books','sport') == ['B', 'B', 'G', 'B', 'Y' ])
    assert(words.compare('sport','books') == ['Y', 'B', 'G', 'B', 'B' ])