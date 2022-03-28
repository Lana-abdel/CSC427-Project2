UNK = None 

#sampleInput = open("test.txt", "r") 


#tokenization, normalization, sentence segmentation
def preProcessing(file):
    #lowercase everything
    sampleInput = open(file, 'r').read().lower()
    #print(sampleInput)

    #change numbers to NUM
    for word in sampleInput.split():
        if(word.isdigit() == True):
            sampleInput = sampleInput.replace(word, "NUMBER") 

    #sentence segmentation 
    

    #print(sampleInput)
    #sampleInput.close()
    return sampleInput 
    

    
preProcessing("test.txt")

class UnigramModel: 
    def __init__ (self):
        self.sentences = preProcessing("test.txt")
        self.word_count = 0
        self.unigram_count = {} 
        for word in self.sentences.split():
            #print(word)
            self.word_count += 1
            if word in self.unigram_count:
                self.unigram_count[word] = self.unigram_count.get(word) + 1
            else:      
                self.unigram_count[word] = 1
        for item in self.unigram_count:
            print("Key : {} , Value : {}".format(item,self.unigram_count[item]/self.word_count))
    
    def wordCount(self, word):
        return self.unigram_count[word]

class BigramModel(UnigramModel):
    def __init__ (self, sentences):
        UnigramModel.__init__(self) 
        self.sentence = sentences
        self.bigram_count = {}
        self.bigramProbabilities = {}
        
    def calculate_bigram(self):
        previousWord = None
        for word in self.sentence.split():
            #print(word)  
            #previousWord = None
            if previousWord != None:
                #print("previousWord")
                if (previousWord,word) in self.bigram_count: 
                    #print("EeEEEEEEEEEEEEEEEEEEEEE")
                    self.bigram_count[(previousWord,word)] = self.bigram_count.get((previousWord,word)) + 1
                else:    
                    #print("EeEEEEEEEEEEEEEEEEEEEEE")
                    self.bigram_count[(previousWord,word)] = 1
                    
            previousWord=word
        
       # print(self.bigram_count[("<s>", "hi")])
        for (item, item2) in self.bigram_count:
            #print("item1: " , item)
            #print("item2: " , item2))
            print("Key : {} , Value : {}".format((item, item2),self.bigram_count[(item,item2)]/self.unigram_count[item]))
            self.bigramProbabilities[(item, item2)] = self.bigram_count[(item,item2)]/self.unigram_count[item]
            #print (self.bigramProbabilities[(item, item2)])

#processedFile = preProcessing()
umodel = BigramModel(preProcessing("test.txt")) 
umodel.calculate_bigram()
