import pylab


WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=25):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    prop = []
    for word in wordList:
        c = 0.0
        for letter in word:
           if letter in 'aeoui':
                c+=1.0
        prop.append(float(c)/len(word))
        
    mean = sum(prop)/len(prop)
    tot = 0.0
    for i in prop:
        tot += (i - mean)**2
    sd = (tot/len(prop))**0.5
    
    
    pylab.title('The proportion of vowels in each word in wordList')
    pylab.xlabel('% of vowels per word')
    pylab.ylabel('Number of words')
    xmin,xmax = pylab.xlim()
    ymin,ymax = pylab.ylim()
    pylab.text(xmin+ (xmax-xmin)*0.76, 18000/2,
               'Mean = ' + str(round(mean, 4))
               + '\nSD = ' + str(round(sd, 4)))
    pylab.hist(prop, numBins)
    pylab.xlim(0.0, 1.0)
    pylab.show()

if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
