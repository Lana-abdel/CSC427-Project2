# CSC427-Project2 

# Authors: Lana Abdelmohsen, Jared Schmidt, Ben Lifshey, Humza Zaki

# Description 
An implementation of MLE and Add-1 smoothing for sentence generation and perplexity calculation. 

# What you will find  
- main.py: Our main source code for MLE and Add-1 calculations
    - Code description:
      - preProcessing(...): This method will preprocess the training or testing files. 
        - We remove all special characters (based on a hardcoded list).
        - We make everything lowercase and perform sentence segmentation. 
        - This method also handles abbreviations based on a hardcoded abbreviations list.
        - This method also performs <UNK> conversion for the training set.
      - changeTrainingUNK(...): Only used for an already preprocessed dataset. Takes in a sampleInput file as a parameter. This method converts words that appear less times than the UNK_CUTOFF to <UNK>.
      - UnigramModel class: Initializes the unigram model and calculates the MLE and Add-1 probabilities.
      - BigramModel class: Initializes the bigram model and has a function that calculates the MLE and Add-1 probabilities. 
      - generateUnigramSentence(...): Takes in the unigram model object as a parameter. It uses weighted selection to generate a sentence using the unigram model.
      - generateBigramSentence(...): Takes in the bigram model object as a parameter. It uses weighted selection to generate a sentence using the bigram model.
      - calculatePerplexityUnigram(...): Calculates perplexity. Takes the test set and the unigram model object as a parameter.
      - calculatePerplexityBigram(...): Calculates perplexity. Takes the test set and the bigram model object as a parameter. 
      - def checkTestUNK(...): Helper method for calculating bigram perplexity. ***

- The corpora obtained were from this link: http://www.nltk.org/nltk_data/. In this directory, you will find two folders: 
  1. webtext: This is where you will find the test and training files for this corpus. We only used the pirates.txt file, which is the movie script from Pirates of the Caribbean: Dead Man's Chest. 
        - Then we split the pirates.txt file into piratesTEST.txt and piratesTRAINING.txt (these are the two files that you will find inside this folder). The test and training sets were split manually (80-20 split).
  2. genesis: This is where you will find the test and training files for this corpus. We only used the english-web.txt file. 
        - Then we split that file into englishTEST.txt and englishTRAINING.txt (these are the two files that you will find inside this folder). The test and training sets were split manually (80-20 split). 

- D2.pdf: This is where you will find the analysis for tasks 5 to 8. 
 
- D3.pdf: a pdf file that responds to the following questions: 
    - What was easy about this assignment?
    - What was challenging about this assignment or parts that you couldn't get working correctly?
    - What did you like about this assignment?
    - What did you dislike about this assignment?
    - How did your team function? Include details regarding what each team
      member contributed, how the team communicated with each other, and
      how team software development & design was accomplished. 
    - What did you learn from this assignment?

# Instructions For Command Line 

1. on OnDemand, go to your file Home Directory and upload "main.py". Then in the HPC terminal, enter: 

> module add python/3.8.6

> python main.py path1 path2 yes 

The command line takes in three parameters: 
- path1 is the path to the training file
- path2 is the path to the test set file
- yes, indicates that you want to apply the preprocessing we implemented on your corpus otherwise type no like so:

> python main.py path1 path2 no


An example of how to write the path is below: 

> python main.py 'genesis/englishTRAINING.txt' 'genesis/englishTEST.txt' yes  

# The Output
The output on the terminal will include: 
  - The sentences generated for smoothed and unsmoothed bigrams and unigrams
  - The perplexity for smoothed bigrams and unigrams
  - If you choose to use our preprocessing implementation, two files will be generated, tempOut.txt and tempOut2.txt, that are generated from the training/testing files themselves when preprocessing and passed internally through parameters (they are not relevant to the final output as they are just the transformed training/test files and they will be overwritten every time you run the code).
    - we did this to reduce the time complexity of preprocessing large files. 
  - It is important to note that for very large corpora, the program may take a few minutes to run (for example, running a corpus of 13000 lines for training would take a few minutes).
  - For very large corpora, the program may use a large amount of memory as it needs to store all possible bigram probabilities. 
