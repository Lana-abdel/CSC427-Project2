import random  
import math 
import os
import sys

UNK_CUTOFF = 1
    
def changeTrainingUNK(sampleInput):
    specificWordCount = {}
    #count each specific word
    for word in sampleInput.split():
        #print(i)  
        if word in specificWordCount:
            specificWordCount[word] = specificWordCount.get(word) + 1
        else:
            specificWordCount[word] = 1
        
    print("unk step 1 done")
    #check word appearances to change to <UNK> or not
    for word in sampleInput.split():
        if specificWordCount[word] <= UNK_CUTOFF:
            sampleInput = sampleInput.replace(" " + word + " ", " <UNK> ")
    #print(specificWordCount)
    print ("unk step2 done")
    return sampleInput

#tokenization, normalization, sentence segmentation
def preProcessing(file, isTrainingSet = True): 
    specificWordCount = {} #word type count prior to normalization
    special_characters = ['"','#','$','%','&','(',')','*','+','/',':',';','<','=','>','@','[','\\',']','^','`','{','|','}','~','\t'] 

    abbreviations = ["approx." , "appt." , "apt." , "a.d.", "a.s.a.p." , "b.y.o.b." , "b.c.", "dept." , "d.i.y." , "d.c", "est."  , "e.t.a."  
        , "min." , "misc."  , "mr."  , "mrs." , "no."  , "r.s.v.p." , "tel. "  , "temp." , "vet." , "vs.", "ave." , "blvd.", 
        "cyn.", "dr. " , "ln." , "rd." , "st." , "e.g.", "i.e."  , "p.s.", "al.", "u.s.a.", "u.s.", "u.k." ]

    #lowercase everything
    sampleInput = open(file, 'r').read().lower()
    """
    fout = open("c.txt", "wt")

    for line in sampleInput:
        for word in line.split(): 
            print(word)
            line = line.replace(word, "Hi")
            #print(line)
        fout.write( line )

    fout.close()
    fout = open('b.txt', 'r').readlines()
    #for line in fout:
        #for word in line.split(): 
            #print(line)"""

    for i in special_characters:
        sampleInput = sampleInput.replace(i, '')
    #sentence segmentation
    sampleInput = "<s> " + sampleInput 

    #change numbers to NUM 
    for word in sampleInput.split():
        if(word.isdigit() == True):
            sampleInput = sampleInput.replace(word, "NUMBER") 
    print("step 1 done")
    if isTrainingSet:
        #call method 
        sampleInput = changeTrainingUNK(sampleInput)
    print("step 2 done")

    #get rid of !, ?, ',' , and replace with </s> 
    for word in sampleInput.split():
        sampleInput = sampleInput.replace(word, word.rstrip(",")) 
        if word.find("!") != -1: 
            sampleInput = sampleInput.replace(word, word.rstrip("!") + " </s> <s>") 
        if word.find("?") != -1: 
            sampleInput = sampleInput.replace(word, word.rstrip("?") + " </s> <s>")  
        if word.find(".") != -1:
            if word not in abbreviations: 
                sampleInput = sampleInput.replace(word, word.rstrip(".") + " </s> <s>") 
    print("step 3 done")


    if(sampleInput[-3:] == "<s>"):
        return sampleInput[:-4]
    else:
        return sampleInput + " </s>"

def preProcessingNew(file, isTrainingSet = True): 
    specificWordCount = {} #word type count prior to normalization
    special_characters = ['"','#','$','%','&','(',')','*','+','/',':',';','<','=','>','@','[','\\',']','^','`','{','|','}','~','\t'] 

    abbreviations = ["approx." , "appt." , "apt." , "a.d.", "a.s.a.p." , "b.y.o.b." , "b.c.", "dept." , "d.i.y." , "d.c", "est."  , "e.t.a."  
        , "min." , "misc."  , "mr."  , "mrs." , "no."  , "r.s.v.p." , "tel. "  , "temp." , "vet." , "vs.", "ave." , "blvd.", 
        "cyn.", "dr. " , "ln." , "rd." , "st." , "e.g.", "i.e."  , "p.s.", "al.", "u.s.a.", "u.s.", "u.k." ]

    sampleInput = open(file, 'r').readlines()
    fout = open("c.txt", "wt")

    #first start tag

    fout.write("<s> ")

    for line in sampleInput:
        #lowercase the line
        line = line.lower()
        #special characters
        for i in special_characters:
            line = line.replace(i, '')
        #change numbers
        for word in line.split(): 
            line = line.replace(',', '')
            if(word.isdigit() == True):
                line = line.replace(word, "NUMBER")
            if word.find("!") != -1: 
                line = line.replace(word, word.rstrip("!") + " </s> <s>") 
            if word.find("?") != -1: 
                line = line.replace(word, word.rstrip("?") + " </s> <s>")  
            if word.find(".") != -1:
                if word not in abbreviations: 
                    line = line.replace(word, word.rstrip(".") + " </s> <s>") 
            
        fout.write(line)

    #sampleInput.close()
    fout.close()

    fIn = open("c.txt", "rt").readlines()
    fout2 = open("d.txt", "wt")
    
    

    #UNK FUNK
    if(isTrainingSet):
        for line in fIn:
            #print(line)
            for word in line.split(): 
                if word in specificWordCount:
                    specificWordCount[word] = specificWordCount.get(word) + 1
                else:
                    specificWordCount[word] = 1

        for line in fIn:
            for word in line.split(): 
                if specificWordCount[word] <= UNK_CUTOFF:
                    line = line.replace( " " + word + " ", " <UNK> ")
            fout2.write(line)  
    
    """if(fIn[-1][-3:] == "<s>"):
        fIn[-1] = fIn[-1][-4:]
        open("d.txt", 'w').writelines(fIn)
    else:
        fout2.write(" </s>")"""

    fout2.close()
    if(isTrainingSet):
    	preprocessedData = open("d.txt", "r").read()
    else:
    	preprocessedData = open("c.txt", "r").read()
    
    #fout = open('c.txt', 'r').readlines()
    #for line in fout:
        #for word in line.split(): 
            #print(line)

    return preprocessedData

    
 
class UnigramModel: 
    def __init__ (self, sentences, smoothed = False):
        
        self.sentences = sentences
        self.word_count = 0
        self.unigram_count = {} #token count (after normalization)
        self.unigram_probabilities = {}
        self.smoothed = smoothed
        for word in self.sentences.split():
            self.word_count += 1
            if word in self.unigram_count:
                self.unigram_count[word] = self.unigram_count.get(word) + 1
            else:      
                self.unigram_count[word] = 1
        
        if self.smoothed:
            for item in self.unigram_count: 
                #if add1 smoothing
                self.unigram_probabilities[item] = (self.unigram_count[item]+1)/(self.word_count + len(self.unigram_count))
        else:
            for item in self.unigram_count: 
                #MLE (unsmoothed)
                self.unigram_probabilities[item] = self.unigram_count[item]/self.word_count 
        
        #print("Unigram:")
        #print(self.unigram_probabilities)
    
        
class BigramModel(UnigramModel):
    def __init__ (self, sentences, smoothed = False):
        UnigramModel.__init__(self, sentences, smoothed) 
        self.sentence = sentences
        self.bigram_count = {}
        self.bigram_probabilities = {}
        self.smoothed = smoothed
        
    def calculate_bigram(self):
        previous_word = None
        for word in self.sentence.split():  
            if previous_word != None:
                if (previous_word,word) in self.bigram_count: 
                    self.bigram_count[(previous_word,word)] = self.bigram_count.get((previous_word,word)) + 1
                else:    
                    self.bigram_count[(previous_word,word)] = 1
                    
            previous_word=word

        if self.smoothed:                                                                                                 
            for (item, item2) in self.bigram_count:
                self.bigram_probabilities[(item, item2)] = (self.bigram_count[(item,item2)]+1)/(self.unigram_count[item]+ len(self.unigram_count))
        else: 
            for (item, item2) in self.bigram_count:
                self.bigram_probabilities[(item, item2)] = self.bigram_count[(item,item2)]/self.unigram_count[item]
    
        print("Bigram:")
        print(self.bigram_probabilities)

def generateUnigramSentence(umodel): 
    sentence = "<s>" 
    currentWord= "<s>"
    lowestDifference = 1
    while (currentWord != "</s>"):
        for item in umodel.unigram_probabilities: 
            rand = random.uniform(0,1)
            if (abs(umodel.unigram_probabilities[item] - rand) < lowestDifference): 
                lowestDifference = abs(umodel.unigram_probabilities[item] - rand)
                currentWord = item
        sentence = sentence + " " + currentWord
        lowestDifference = 1 
    print("Unigram Sentence:")
    print(sentence)

def generateBigramSentence(umodel):
    sentence = "<s>"
    previous = "<s>"  
    lowestDifference = 1
    next_word = ""
    while(previous != "</s>"):
        for (item,item2) in umodel.bigram_probabilities:
            rand = random.uniform(0,1)
            if(item == previous):
                #weighted avg
                if (abs(umodel.bigram_probabilities[previous,item2] - rand) < lowestDifference):
                    lowestDifference = abs(umodel.bigram_probabilities[previous,item2] - rand)
                    next_word = item2 
        previous = next_word
        sentence = sentence + " " + next_word
        #print(sentence)
        lowestDifference = 1
    print("\nBigram Sentence:")
    print(sentence) 

def calculatePerplexityUnigram(testSet, umodel): 
    #currentWord = None 
    perplexitySum = 0
    perplexity = 0 
    for word in testSet.split(): 
        try:
            perplexitySum +=  math.log(umodel.unigram_probabilities[word],2)
        except:
            perplexitySum +=  math.log(umodel.unigram_probabilities["<UNK>"],2)
    perplexity = math.pow(2, (-1/len(testSet.split()) * perplexitySum))
    print("\nUnigram Perplexity:")
    print(perplexity)

def calculatePerplexityBigram(testSet, umodel):
    previousWord = None
    currentWord = None
    doneFirstWords = False
    perplexitySum = 0
    perplexity = 0
    for word in testSet.split():
        #print(word)
        if(not doneFirstWords):
            if previousWord == None:
                previousWord = word
            else: 
                currentWord = word
                doneFirstWords = True
        else:
            #exp(-1/n * sum(logP(wi|wi-1))
            perplexitySum = checkTestUNK(umodel,perplexitySum,previousWord,currentWord)
            previousWord = currentWord
            currentWord = word 
            
    perplexitySum = checkTestUNK(umodel,perplexitySum,previousWord,currentWord)
    perplexity = math.pow(2, ((-1/len(testSet.split())) * perplexitySum))
    print("\nBigram Perplexity:")
    print(perplexity)
            
def checkTestUNK(umodel, perplexitySum, previousWord, currentWord):
    try:
        perplexitySum +=  math.log(umodel.bigram_probabilities[previousWord, currentWord],2)
    except:
        try:
            perplexitySum +=  math.log(umodel.bigram_probabilities["<UNK>", currentWord],2)
        except:
            try:
                perplexitySum +=  math.log(umodel.bigram_probabilities[previousWord, "<UNK>"],2)
            except:
                perplexitySum +=  math.log(umodel.bigram_probabilities["<UNK>", "<UNK>"],2)
    return perplexitySum
    

#processedFile = preProcessing()
trainFile = sys.argv[1]
testFile = sys.argv[2]
#umodel = BigramModel(preProcessing(inputFile), smoothed= False)  
preprocessingFlag = sys.argv[3].lower()

if preprocessingFlag == 'yes' :
    print("HI")
    umodel = BigramModel(preProcessingNew(trainFile), smoothed= False) 
    umodel.calculate_bigram() 
    generateUnigramSentence(umodel) 
    generateBigramSentence(umodel)
    calculatePerplexityBigram(preProcessingNew(testFile, isTrainingSet=False), umodel)
    calculatePerplexityUnigram(preProcessingNew(testFile, isTrainingSet=False), umodel)
else:
    testFile = open(testFile, "r").read()
    trainFile = open(trainFile, "r").read()
    umodel = BigramModel(changeTrainingUNK(trainFile), smoothed= True) 
    umodel.calculate_bigram() 
    generateUnigramSentence(umodel) 
    generateBigramSentence(umodel)
    calculatePerplexityBigram(testFile, umodel)
    calculatePerplexityUnigram(testFile, umodel)


#preProcessingNew("toycorpuswecreated/test.txt")
