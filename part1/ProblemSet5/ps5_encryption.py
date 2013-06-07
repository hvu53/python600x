# 6.00x Problem Set 5
#
# Part 1 - HAIL CAESAR!

import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList

def isWord(wordList, word):
    """
    Determines if word is a valid word.

    wordList: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordList.

    Example:
    >>> isWord(wordList, 'bat') returns
    True
    >>> isWord(wordList, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def randomWord(wordList):
    """
    Returns a random word.

    wordList: list of words  
    returns: a word from wordList at random
    """
    return random.choice(wordList)

def randomString(wordList, n):
    """
    Returns a string containing n random words from wordList

    wordList: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([randomWord(wordList) for _ in range(n)])

def randomScrambled(wordList, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordList: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words

    NOTE:
    This function will ONLY work once you have completed your
    implementation of applyShifts!
    """
    s = randomString(wordList, n) + " "
    shifts = [(i, random.randint(0, 25)) for i in range(len(s)) if s[i-1] == ' ']
    return applyShifts(s, shifts)[:-1]

def getStoryString():
    """
    Returns a story in encrypted text.
    """
    return open("story.txt", "r").read()


# (end of helper code)
# -----------------------------------


#
# Problem 1: Encryption
#
def buildCoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation, numbers and spaces.

    shift: 0 <= int < 26
    returns: dict
    """
    ### TODO.
    lower = dict.fromkeys(string.ascii_lowercase, 0)
    upper = dict.fromkeys(string.ascii_uppercase, 0)
        
    for i in lower:
        if (ord(i) + shift) > 122:
            lower[i] = chr(ord(i) - (122-96) + shift)
        else:
            lower[i] = chr(ord(i) + shift)        

    for k in upper:
        if (ord(k) + shift) > 90:
            upper[k] = chr(ord(k) - (90-64) + shift)
        else:
            upper[k] = chr(ord(k) + shift)
            
    both = dict(lower.items() + upper.items())
    return both

def applyCoder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text
    """
    ### TODO.
    text2 = ''
    for word in text:
        if coder.has_key(word):
            word = coder[word]
            text2 += word
        else:
            text2 += word
    return text2
       

def applyShift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. Lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text (0 <= int < 26)
    returns: text after being shifted by specified amount.
    """
    ### TODO.
    ### HINT: This is a wrapper function.
    return applyCoder(text,buildCoder(shift))

#
# Problem 2: Decryption
#
def findBestShift(wordList, text):
    """
    Finds a shift key that can decrypt the encoded text.

    text: string
    returns: 0 <= int < 26
    """
    ### TODO

    #1. Set the maximum number of real words found to 0.
    maxword = 0
    #2. Set the best shift to 0.
    bestshift =0

    #3. For each possible shift from 0 to 26:
    for eachshift in range(0, 26):
        validword = 0
        #4. Shift the entire text by this shift.
        texts = applyShift(text, eachshift)
        #5. Split the text up into a list of the individual words.
        textlist = texts.split(" ")
        #6. Count the number of valid words
        for i in textlist:
            if isWord(wordList,i):
                validword +=1
        #7. If this number of valid words is more than the largest number of
	   #real words found, then:
        if validword > maxword:
            #8. Record the number of valid words.
            maxword = validword
            #9. Set the best shift to the current shift.
            bestshift = eachshift
            
    #11. Return the best shift.
    #return bestshift
    return bestshift
def decryptStory():
    """
    Using the methods you created in this problem set,
    decrypt the story given by the function getStoryString().
    Use the functions getStoryString and loadWords to get the
    raw data you need.

    returns: string - story in plain text
    """
    ### TODO.
##    text = getStoryString()
##    wordLists = loadWords()
##    shift = findBestShift(wordLists, text)
##    return applyShift(text, shift)
##    wordList = loadWords()
##    text = getStoryString()
##    shift = findBestShift(wordList, text)
##    return applyShift(text, shift)
    return 'not implemented'
#
# Build data structures used for entire session and run encryption
#

if __name__ == '__main__':
    wordList = loadWords()
    decryptStory()
