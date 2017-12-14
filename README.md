Natawut Monaikul, Anne Huang
CS 521 Project
Fall 2017

All of the code is in the Code directory. This code was prepared using the scientific distribution of Python. The specific modules that need to be installed to run this code include nltk, sklearn and lda, among others.

We also use the GitHub repository BTM, the Stanford CoreNLP toolkit, and the Stanford Politeness API.

Included are three modules: ParseFiles.py, model.py, and ScriptFunctions.py.

ScriptFunctions.py is the original code file we used to extract movie scripts and lines from imsdb.com, the Internet Movie Script Database. It includes functions to extract specific lines spoken by specific characters from the movie script as an HTML file (so we had to manually infer the gender of characters), as well as to clean up the lines by removing unnecessary characters, etc. After we found the Cornell Movie-Script Dialogue Corpus, we no longer needed these functions, so we instead created ParseFiles.py.

ParseFiles.py has all of the functions we used to create the files of spoken lines split by gender and genre from the original corpus, read the files into a format that can be used as input to the topic models and the politeness classifier, and run the topic models. Running the code all the way through would require running the functions for each of these steps in order; however, we found that the code for the politeness classifier requires older versions of some packages, while the code for the topic models requires newer versions, so we had to externally perform the intermediate steps of downgrading and upgrading packages for the code to work.

model.py has all of the functions to run the politeness classifier (though it calls other modules not included here because they were not modified by us). This module is taken from the creators of the politeness classifier, but it has been modified to integrate other code from the creators and to format the input and output accordingly.

The functions for creating the files of spoken lines split by gender and genre involved linking IDs from each of the files in the original corpus, since the corpus was split into a file of movies, a file of characters, a file of lines, etc. The functions for reading the files into the proper format included removing characters that were not in the standard 128 ASCII characters, tokenizing, stop-word removal, and stemming for the topic models. There are also functions to use the Stanford Parser, draw 500 random lines from the data for parsing, and modify the output of the parser to match what's expected by the politeness classifier. The functions to run the topic models include that which performs LDA from a file, where each line is considered a document. The code to run BTM was taken directly from the creators' Github, though we did have to modify it to make it compatible with Python 2 isntead of 3, and to take our input files instead of their sample one. This code is not included since it was not one we wrote. 

The functions to run the politeness classifier include checking if a sentence is a request (provided by the creators but integrated into a single file), reading in the parser output from a file, running the actual classifier which has already been trained (the file specifying the model from the creators is not included here), and outputting statistics of the classifier output (average, number of requests vs. lines, t-test).
