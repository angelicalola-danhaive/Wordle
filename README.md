# Wordle Solver

This is a code that allows the user to play Wordle in two main ways: either by giving the code a word and letting solve for it, or by playing interactively and guessing a word generate randomly by the code. In this latter case, the code will help you find the solution by suggesting guesses.

## Contents
The following files are contained in this project:
 - `wordle_solver.py` : contains the body of the code
 - `words.py`: module containing functions that handle and compare words
 - `probabilities.py`: module containing functions that computing the different probabilities and scores associated to each word
 - `game.py`: module containing functions necessary to operate the game, such as generating guessing and testing them against the solution
 - `WordleWords.txt` : the full list of possible 5-letter words that Wordle (and this code) accepts
 - `requirements.txt` : the list of modules to be installed. This is done automatically in both the continuous integration and Docker frameworks
 - `Dockerfile` : the Dockerfile to run this entire code on any machine
    
Each module also has the corresponding test file where all of the unit tests for the functions are stored.

## Installation

This code can be downloaded as a Docker project and hence be run on any machine. The `Dockerfile` can be found in this repository. To run the code:
 - Go in the directory where the Dockerfile is on your local machine:
 
   ```bash
      cd docker_directory
   ```
 - Create your image from the Dockerfile (replace `image_name` with the name you want to give to your image)
 
    ```bash
      docker build -t image_name .
   ```
 - Create your container from the image
    ```bash
      docker run --rm -ti image_name
   ``` 
 - the Dockerfile automatically clones this repository in your local directory, so you can now directly run your  `wordle_solver.py`. 
 
Alternatively, you can clone this repository manually:

    ```bash
      cd wordle_directory
      git clone https://github.com/angelicalola-danhaive/Wordle.git
   ```
If you chose to do this, make sure you have installed python3.9, git, pandas, and matplotlib.

## How to run
Running the code is simple. 
 - Run `wordle_solver.py` from the command line:
    
   ```bash
      python wordle_solver.py
   ```
 - First you will be asked if you want to simply run the code over all of the words in the list. This is useful to see how quickly the code can solve a Wordle on average. If yes, enter **'run'**, if not, simply press *ENTER* to be taken to the main version. If you press *ENTER* then:
    - you will be asked which version of the game you want to play, enter **'interact'** if you want to try to guess the computer-generated word, or **'solve'** if you want the computer to solve a word you input
    - In the latter case, the code will run by itself until the solution you entered is found
    - If you are guessing, then the computer will suggest a guess, which you are free to use or type in any other 5-letter word to guess. You can type **'more'** if you want to see the list of all possible words at this stage of the game.

If you enter **'run'** then the code will loop over all of the words in WordleWords.txt and count how many guesses it takes to solve for each one. The results are plotted in a histogram at the end, the average number of tries is printed. 

## Features

This code allows you to do the following things:

 - Solve for any 5-letter word in the WordleWords.txt 
 - Play Wordle yourself by choosing the interactive option
 - Running the solver over all of the words in WordleWords.txt to compute the average amount of guesses it takes to solve a word
 
 In both cases, the code generates the best next guess by computing the frequencies of letters in all of the remaining words. It then picks as next guess the word with the most frequent letters. For the second guess, it also makes sure to pick a word with all different letters from the first.


## Frameworks
This entire project is coded in Python. Most of the functions in the different modules have corresponding unit tests found in the `wordle_module.py` files. If you edit this code in your local repository, you can run these tests to check the functions still work correctly. Either
    
   ```bash
      pytest
   ```
to run all of them or 
    
   ```bash
      pytest test_module.py
   ```
to only run the tests for a specific module.
These unit tests are implemented through a continuous integration in GitHub repository so that commits from the development branch can only be merged with the main if all of the unit tests pass. 







