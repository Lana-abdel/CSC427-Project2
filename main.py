#Authors: Lana Abdelmohsen, Jared Schmidt, Ben Lifshey, Humza Zaki
import random  
import math 
import sys

UNK_CUTOFF = 2 

#method that converts words that appear less times than the UNK_CUTOFF to <UNK>
def changeTrainingUNK(sampleInput):
    specificWordCount = {} #word type count prior to normalization
    tempIn = open(sampleInput, "rt").readlines()
    #second temp file if needed to write preprocressed input with <UNK> to
    tempOutput2 = open("tempOut2.txt", "wt")
    
    for line in tempIn:
        for word in line.split(): 
            if word in specificWordCount:
                specificWordCount[word] = specificWordCount.get(word) + 1
            else:
                specificWordCount[word] = 1

    for line in tempIn:
        for word in line.split(): 
            if specificWordCount[word] <= UNK_CUTOFF:
                line = line.replace( " " + word + " ", " <UNK> ")
        tempOutput2.write(line)  

    tempOutput2.close()

    preprocessedData = open("tempOut2.txt", "r").read()

    return preprocessedData


def preProcessing(file, isTrainingSet = True): 
    specificWordCount = {} #word type count prior to normalization
    special_characters = ['"','#','$','%','&','(',')','*','+','/',':',';','<','=','>','@','[','\\',']','^','`','{','|','}','~',',','\t'] 

    abbreviations = ["approx." , "appt." , "apt." , "a.d.", "a.s.a.p." , "b.y.o.b." , "b.c.", "dept." , "d.i.y." , "d.c", "est."  , "e.t.a."  
        , "min." , "misc."  , "mr."  , "mrs." , "no."  , "r.s.v.p." , "tel. "  , "temp." , "vet." , "vs.", "ave." , "blvd.", 
        "cyn.", "dr. " , "ln." , "rd." , "st." , "e.g.", "i.e."  , "p.s.", "al.", "u.s.a.", "u.s.", "u.k." ] #list of recognized abbreviations

    sampleInput = open(file, 'r').readlines()

    #our preprocessing method writes the preprocessed input to a seperate file
    tempOutput = open("tempOut.txt", "wt") 

    
    #first start tag
    tempOutput.write("<s> ")

    #each line is preprocessed individually for performance purposes  
    for line in sampleInput:
        #lowercase the line
        line = line.lower()
        #remove special characters
        for i in special_characters:
            line = line.replace(i, '')
        for word in line.split(): 
            #replace numbers with NUMBER  
            if(word.isdigit() == True):
                line = line.replace(word, "NUMBER")
              #sentence segmentation
            if word.find("!") != -1: 
                line = line.replace(word, word.rstrip("!") + " </s> <s>") 
            if word.find("?") != -1: 
                line = line.replace(word, word.rstrip("?") + " </s> <s>")  
              #if encounter a period check if it is an abbreviation before segmenting
            if word.find(".") != -1:
                if word not in abbreviations: 
                    line = line.replace(word, word.rstrip(".") + " </s> <s>") 
            
        tempOutput.write(line)
      
    tempOutput.close()

    tempIn = open("tempOut.txt", "rt").readlines()
    #second temp file if needed to write preprocressed input with <UNK> to
    tempOutput2 = open("tempOut2.txt", "wt")
    
    

    #performs <UNK> conversion for training set
    if(isTrainingSet):
        for line in tempIn:
            for word in line.split(): 
                if word in specificWordCount:
                    specificWordCount[word] = specificWordCount.get(word) + 1
                else:
                    specificWordCount[word] = 1

        for line in tempIn:
            for word in line.split(): 
                if specificWordCount[word] <= UNK_CUTOFF:
                    line = line.replace( " " + word + " ", " <UNK> ")
            tempOutput2.write(line)  

    tempOutput2.close()
    #<UNK> conversion not needed for test set so only the initial temp file is utilized for the test set
    if(isTrainingSet):
    	preprocessedData = open("tempOut2.txt", "r").read()
    else:
    	preprocessedData = open("tempOut.txt", "r").read()
      
    return preprocessedData

     
class UnigramModel: 
    #initialize the unigram model
    def __init__ (self, sentences, smoothed = False):
        self.sentences = sentences
        self.word_count = 0
        self.unigram_count = {} #token count (after normalization)
        self.unigram_probabilities = {}
        self.smoothed = smoothed #smoothed set to false as default
       
      #get count of each unigram
        for word in self.sentences.split():
            self.word_count += 1
            if word in self.unigram_count:
                self.unigram_count[word] = self.unigram_count.get(word) + 1
            else:      
                self.unigram_count[word] = 1

        #calculate probabilty of each unigram 
        if self.smoothed: #if add-one smoothing
            for item in self.unigram_count: 
                self.unigram_probabilities[item] = (self.unigram_count[item]+1)/(self.word_count + len(self.unigram_count))
        else: #MLE (unsmoothed)
            for item in self.unigram_count: 
                self.unigram_probabilities[item] = self.unigram_count[item]/self.word_count 
        
    
        
class BigramModel(UnigramModel):
    #initialize the bigram model
    def __init__ (self, sentences, smoothed = False):
        UnigramModel.__init__(self, sentences, smoothed) 
        self.sentence = sentences
        self.bigram_count = {}
        self.bigram_probabilities = {}
        self.smoothed = smoothed
      
    def calculate_bigram(self):
        #get count of each bigram
        previous_word = None
        for word in self.sentence.split():  
            if previous_word != None:
                if (previous_word,word) in self.bigram_count: 
                    self.bigram_count[(previous_word,word)] = self.bigram_count.get((previous_word,word)) + 1
                else:    
                    self.bigram_count[(previous_word,word)] = 1
                    
            previous_word=word

        #calculate probabilities of each bigram 
        unigramLength = len(self.unigram_count) #size of vocabulary
        if self.smoothed: #if add-one smoothing                                                                                                 
            for item in self.unigram_count:
                for item2 in self.unigram_count:
                    if (item, item2) in self.bigram_count: #bigrams that appear in training data
                        self.bigram_probabilities[(item, item2)] = (self.bigram_count[(item,item2)]+1)/(self.unigram_count[item]+ unigramLength)
                    else: #bigrams that don't appear in training data
                        self.bigram_probabilities[(item, item2)] = (1/(self.unigram_count[item]+ unigramLength))
        else: #MLE (unsmoothed)
            for item in self.unigram_count:
                for item2 in self.unigram_count:
                    if (item, item2) in self.bigram_count: #bigrams that appear in training data 
                        self.bigram_probabilities[(item, item2)] = (self.bigram_count[(item,item2)])/(self.unigram_count[item])
                    else: #bigrams that don't appear in training data
                        self.bigram_probabilities[(item, item2)] = 0

#generate a sentence using the unigram model and weighted selection                      
def generateUnigramSentence(umodel): 
    sentence = "<s>" 
    currentWord= "<s>"

    probabilitesList = []
    dictWords = {}
    addProb = 0
  
    #create the number line
    for item in sorted(umodel.unigram_probabilities.values(), reverse = True): 
        addProb = item + addProb
        probabilitesList.append(addProb)
   #associate each unigram with its respective interval in the number line
    i = 0
    for value in sorted(umodel.unigram_probabilities, key = umodel.unigram_probabilities.get, reverse = True):
        dictWords[i] = value
        i += 1
      
    #generate random number and add word to sentence based on where random number fits in number line
    while (currentWord != "</s>"):
        rand = random.uniform(0,1)
        for j in range(len(probabilitesList)):
            if(rand < probabilitesList[j]):
                currentWord = dictWords[j]
                break     

        sentence = sentence + " " + currentWord

    print("Unigram Sentence:")
    print(sentence)

#generate a sentence using the bigram model and weighted selection
def generateBigramSentence(umodel, cutoff=False):
    sentence = "<s>"
    previous = "<s>"
    currentWord = ""
    numWords = 0 
  #too many words can appear before </s> slowing performance with the addition of non-valid bigrams that don't feature the </s>

    #create the number line for each first word in the bigram  
    sortedBigram = sorted(umodel.bigram_probabilities, key = umodel.bigram_probabilities.get, reverse = True)
    while(previous != "</s>"):
        probabilitesList = []
        dictWords = {}
        addProb = 0
        for (item,item2) in umodel.bigram_probabilities:
            if(item == previous): 
                probabilitesList.append(umodel.bigram_probabilities[(item, item2)])

        probabilitesList= sorted(probabilitesList, reverse = True)
        probabilitesList2 = []
        for i in range(len(probabilitesList)):
            addProb += probabilitesList[i]
            probabilitesList2.append(addProb)
        #associate each possible second word in bigram with its respective interval in the number line for the first word
        i = 0
        for value1,value2 in sortedBigram:
            if(value1 == previous):
                dictWords[i] = value2
                i += 1 

        #generate random number and add word to sentence based on where random number fits in number line for the first word
        rand = random.uniform(0,1)
        for j in range(len(probabilitesList2)):
            if(rand < probabilitesList2[j]):
                currentWord = dictWords[j]
                break     
   
        previous = currentWord
        sentence = sentence + " " + currentWord
        numWords += 1
        
      #end sentence if can not encounter </s> tag because many unreal bigrams being considered in add-one smoothing
        if(numWords>=11 and cutoff): 
            sentence = sentence + " </s>"
            break

    print("\nBigram Sentence:")
    print(sentence) 

#calculate perplexity using unigram model
def calculatePerplexityUnigram(testSet, umodel): 
    perplexitySum = 0
    perplexity = 0 
    for word in testSet.split(): 
        try: #word appeared in training set
            perplexitySum +=  math.log(umodel.unigram_probabilities[word],2)
        except: #word did not appear in training set
            perplexitySum +=  math.log(umodel.unigram_probabilities["<UNK>"],2)
    perplexity = math.pow(2, (-1/len(testSet.split()) * perplexitySum))
    print("\nUnigram Perplexity:")
    print(perplexity)

#calculate perplexity using bigram model
def calculatePerplexityBigram(testSet, umodel):
    previousWord = None
    currentWord = None
    doneFirstWords = False
    perplexitySum = 0
    perplexity = 0
    for word in testSet.split():
       #make sure the first two words are properly traversed and added to the calculation
        if(not doneFirstWords): 
            if previousWord == None:
                previousWord = word
            else: 
                currentWord = word
                doneFirstWords = True
        else:
            perplexitySum = checkTestUNK(umodel,perplexitySum,previousWord,currentWord) #checks if bigrams are recongized before adding to sum
            previousWord = currentWord
            currentWord = word 
            
    perplexitySum = checkTestUNK(umodel,perplexitySum,previousWord,currentWord)
    perplexity = math.pow(2, ((-1/len(testSet.split())) * perplexitySum))
    print("\nBigram Perplexity:")
    print(perplexity)

#method that accounts for the test set containing a bigram that did not appear in the training set
def checkTestUNK(umodel, perplexitySum, previousWord, currentWord):
    try: #bigram is recongized
        perplexitySum +=  math.log(umodel.bigram_probabilities[previousWord, currentWord],2)
    except KeyError:
        try: #first word of bigram is unknown
            perplexitySum +=  math.log(umodel.bigram_probabilities["<UNK>", currentWord],2)
        except KeyError:
            try: #second word of bigram is unknown
                perplexitySum +=  math.log(umodel.bigram_probabilities[previousWord, "<UNK>"],2)
            except KeyError: #both words of bigram are unknown
                perplexitySum +=  math.log(umodel.bigram_probabilities["<UNK>", "<UNK>"],2)
    return perplexitySum
    

trainFile = sys.argv[1] #training set
testFile = sys.argv[2] #test set
preprocessingFlag = sys.argv[3].lower() #determines whether to do preprocessing

if preprocessingFlag == 'yes' : #do preprocessing on file
     
    print("\nUnsmoothed\n") 
    umodel = BigramModel(preProcessing(trainFile), smoothed= False) #when BigramModel is called a UnigramModel is also created
    umodel.calculate_bigram() 
    generateUnigramSentence(umodel) 
    generateBigramSentence(umodel, cutoff = False)
  
    print("\nsmoothed\n")
    umodel2 =  umodel = BigramModel(preProcessing(trainFile), smoothed= True) #when BigramModel is called a UnigramModel is also created
    umodel.calculate_bigram() 
    generateUnigramSentence(umodel2) 
    #cutoff only needed for add-one due to the addition of many unreal bigrams to consideration that do not contain the </s> tag
    generateBigramSentence(umodel2, cutoff = True)  
    calculatePerplexityBigram(preProcessing(testFile, isTrainingSet=False), umodel2)
    calculatePerplexityUnigram(preProcessing(testFile, isTrainingSet=False), umodel2)
else:
    print("\nUnsmoothed\n")
  
    #preprocessed file would still not have inclusion of <UNK> leading to the call of the changeTrainingUNK method 
    umodel = BigramModel(changeTrainingUNK(trainFile), smoothed= False) 
    umodel.calculate_bigram() 
    generateUnigramSentence(umodel) 
    generateBigramSentence(umodel)
  
    print("\nsmoothed\n")
    #preprocessed file would still not have inclusion of <UNK> leading to call of changeTrainingUNK method 
    umodel2 =  umodel = BigramModel(changeTrainingUNK(trainFile), smoothed= True) 
    umodel.calculate_bigram() 
    generateUnigramSentence(umodel2) 
    #cutoff only needed for add-one due to the addition of many unreal bigrams to consideration that do not contain the </s> tag
    generateBigramSentence(umodel2, cutoff = True)
    calculatePerplexityBigram(testFile, umodel2)
    calculatePerplexityUnigram(testFile, umodel2)
