Anne Huang, Natawut Monaikul
CS 521 Project
Fall 2017

Our code was prepared using Anaconda, which includes the scientific distribution of Python. The specific modules that need to be installed include nltk, sklearn and lda.

Preconditions for using ScriptFunctions.py:
read_file is a .txt file containing the text of a script.

The functions in ScriptFunctions.py can be imported to be used in Python using:

import ScriptFunctions

ScriptFunctions.output_lines() takes a list of character names, read_file, and a write_file path. For example:
output_lines(["TONY", "IRON MAN", "STEVE", "CAPTAIN AMERICA", "THOR"], "AvengersScript.txt", "Avengers_Male.txt")

This will output all the lines of these characters.

preprocessForBTM.py does some further preprocessing. The paths of output paths produced above are hardcoded. To run the program, use:

import preprocessForBTM

preprocessForBTM.main()

textProcessing.py runs lda on the output from preprocessForBTM.py
To run the program, use:

import textProcessing

preprocessForBTM.glob()

We also used the GitHub repository BTM.
