# Wordle Solver

This is a code that allows the user to play Wordle in two main ways: either by giving the code a word and letting solve for it, or by playing interactively and guessing a word generate randomly by the code. In this latter case, the code will help you find the solution by suggesting guesses.

Motivation??

## Contents
The following files are contained in this project:
 - `wordle_solver.py` : contains the body of the code
 - `words.py`: module containing functions that handle and compare words
 - `probabilities.py`: module containing functions that computing the different probabilities and scores associated to each word
 - `game.py`: module containing functions necessary to operate the game, such as generating guessing and testing them against the solution
    
Each module also has the corresponding test file where all of the unit tests for the functions are stored.

## Installation

This code can be downloaded as a Docker project and hence be run on any machine. The `Dockerfile` can be found in this repository. To run the code:
 - Go in the directory where the Dockerfile is on your local machine:
 
   ```bash
      cd docker_directory
   ```
 - Create your image from the Dockerfile
 
    ```bash
      docker build -t image_name .
   ```
 - Create your container from the image
    ```bash
      docker run --rm -ti conda
   ``` 
 - the Dockerfile automatically clones this repository in your local directory, so you can now directly run your  `wordle_solver.py`. 
 
Alternatively, you can clone this repository manually:
    ```bash
      cd wordle_directory
      git clone https://github.com/angelicalola-danhaive/Wordle.git
    ```
If you chose to do this, make sure you have installed python, git, and pandas.

## How to run
Running the code is simple. 
 - Run `wordle_solver.py` from the command line:
    
   ```bash
      python wordle_solver.py
   ```
 - you will then be asked which version of the game you want to play, enter 'interact' if you want to try to guess the computer-generated word, or 'solve' if you want the computer to solve a word you input
 - In the latter case, the code will run by itself until the solution you entered is found
 - If you are guessing, then the computer will suggest a guess, which you are free to use or type in any other 5-letter word to guess. You can type 'more' if you want to see the list of all possible words at this stage of the game.
    
In 'wordle_solver.py', there is also the option to loop the code over a list of words without inputting anything. To do so, comment out the first outlined block of code and uncomment the bottom section, then run again.

## Features

??

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





