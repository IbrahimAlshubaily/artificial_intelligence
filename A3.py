import random

####################################### word class ################################################
class word:
    def __init__(self, word, count = 1):
        self.word = word
        self.count = count

    def equals(self, theWord):
        if (self.word == theWord):
            return True
        else:
            return False
    def inreaseCount(self):
        self.count += 1
        


####################################### consecative words class #####################################
# Used as value in our key,value dictionary
class consecativeWords:
    def __init__(self, secondWord, thirdWord):
        self.secondWords = list()
        secondWord  = word(secondWord)
        self.secondWords.append(secondWord)
        
        self.thirdWords = list()
        thirdWord  = word(thirdWord)
        self.thirdWords.append(thirdWord)

    def addWord(self , listOfWords,theWord):
        new = True
        for w in listOfWords:
             if w.equals(theWord):
                 new = False
                 w.inreaseCount()
        if new:
            listOfWords.append(word(theWord))

    def getNextWord(self, listOfWords):
        maxCount = 0
        selectedWord = 0
        for word in listOfWords:
            if word.count > maxCount:
                selectedWord = word
                maxCount = word.count
        return selectedWord
      


   
####################################### Generate trigrams ########################################
def getTriGrams(words):
    d = {}
    for i in range (0, len(words)-2):
        trigram = [words[i], words[i+1], words[i+2]]
        #print(trigram)
        if ( trigram[0] in d):
            d[trigram[0]].addWord(d[trigram[0]].secondWords,  trigram[1])
            d[trigram[0]].addWord(d[trigram[0]].thirdWords, trigram[2])
        else :
            d[trigram[0]] = consecativeWords(trigram[1], trigram[2])
    return d



####################################### parse input text #########################################
def parseFile(file_name):
    in_file = open(file_name,"r")
    lines = [[str(i) for i in line.strip().split(',')] for line in open(file_name,"r").readlines()]
    content = ""
    for i in lines:
        content += str(i) + " "
    return content[:-1].replace("[", "").replace("]", "").replace("'", "").lower()



####################################### Generate a 1000 words ####################################
def tellStory(trigrams):
    firstWord = trigrams.keys()[random.randint(0, len(trigrams)-1)]
    i = 1
    w = firstWord
    story = w + " "
    r = 0
    while i < 1000:
        r += 1
        if i < 1000:
            w2 = trigrams[w].getNextWord(trigrams[w].secondWords).word
            story += w2+ " "
            i+=1
        if i < 1000:
            w3 = trigrams[w].getNextWord(trigrams[w].thirdWords).word
            story += w3+ " "
            i+=1

            
        if r >= 5:
            r = 0
            w = trigrams.keys()[random.randint(0, len(trigrams)-1)]
        else:          
            w = w3

    print(story)
    print(len(story.split()))
    return story
        

####################################### main #####################################################
content = parseFile("doyle-27.txt")
content += parseFile("doyle-case-27.txt")
trigrams = getTriGrams(content.split())
out_file = open("Ibrahim_AI_Story1.txt","w")
out_file.write(tellStory(trigrams))

content = parseFile("doyle-27.txt")
content += parseFile("doyle-case-27.txt")
content += parseFile("alice-27.txt")
content += parseFile("london-call-27.txt")
content += parseFile("melville-billy-27.txt")
content += parseFile("twain-adventures-27.txt")

trigrams = getTriGrams(content.split())
out_file = open("Ibrahim_AI_Story2.txt","w")
out_file.write(tellStory(trigrams))
