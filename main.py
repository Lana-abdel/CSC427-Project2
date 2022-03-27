UNK = None 

sampleInput = open("test.txt", "r") 

#print(sampleInput.readlines())

#sampleInput.close()

class UnigramModel: 
    def __init__ (self, sentences):
        self.sentences = sentences
        self.word_count = 0
        self.unigram_count = {} 

    def calculate_unigram(self):
        for sentence in self.sentences:
            sentenceSplit = sentence.split()
            for word in sentenceSplit:
                print(word)
                self.word_count += 1
                if word in self.unigram_count:
                    self.unigram_count[word] = self.unigram_count.get(word) + 1
                else:
                    self.unigram_count[word] = 1
                #print(self.unigram_count[word]/self.word_count)
                #self.unigram_count[word] = self.unigram_count.get(word,0)+1  
        for item in self.unigram_count:
            print("Key : {} , Value : {}".format(item,self.unigram_count[item]/self.word_count))
            #print(self.unigram_count[item]/self.word_count)

umodel = UnigramModel(sampleInput) 
umodel.calculate_unigram()
