import random
import os
hangmanpics = ['''

                +---+
                |   |
                    |
                    |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
                    |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
                |   |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|   |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
               /    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
               / \  |
                    |
                    |
              =========== ''']

Country = 'india australia egypt ghana japan china pakistan afghanistan kenya libya chile'
City = 'bankok bangalore hyderabad newyork shangai berlin calcutta'
Famousp = 'shashank gandhi hitler nehru che jackie brucelee vallabaipatel vivekananda'

def Countries():
    print('You will have to guess the name of a Country')
    return Country

def Cities():
    print('You will have to guess the name of a City')
    return City

def Famous():
    print('You will have to guess this Famous Personality')    
    return Famousp

def err():
    print('You will get a random word from the above 3')
    return Country + City + Famousp

def Welcomenote():

    print('Select One Category')
    print(' 1: Countries')
    print(' 2: Cities')
    print(' 3: Famous Personalities')
    print(' 4: Random') 

    choice = {
        "1": Countries,
        "2": Cities,
        "3": Famous }
    
    choose = input()
    return choice.get(choose,err)().split()

    
def getRandomword(wordlist):
    wordindex = random.randint(0,len(wordlist)-1)
    return wordlist[wordindex]

def display(hangmanpics,missedletters,correctletters,secretword):
    os.system('cls')
    print(hangmanpics[len(missedletters)])
    print()
    
    print("Missed Letters:", end = ' ')
    for letter in missedletters:
        print(letter, end=' ')
    print()
    print()

    blanks = '_' * len(secretword)

    for i in range(len(secretword)):
        if secretword[i] in correctletters:
            blanks = blanks[:i] + secretword[i] + blanks[i+1:]

    for letter in blanks:
        print(letter,end=' ')

    print()
    print()


def getguess(alreadyguessed):
    while True:
        print(' Guess a Letter  ')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter single letters')
        elif guess in alreadyguessed:
            print('This letter is already guessed,choose a new letter')
        else:
            return guess

def playagain():
    print('Do you wanna play again? (Yes or No)')
    return input().lower().startswith('y')

print(' Welcome to  H A N G M A N by SHASHANK')
print(hangmanpics[6])
words = Welcomenote()
missedletters = ''
correctletters = ''
secretword = getRandomword(words)

done = False

while True:
    display(hangmanpics,missedletters,correctletters,secretword)
    guess = getguess(missedletters + correctletters)

    if guess in secretword:
        correctletters = correctletters + guess
        found = True
        for i in range(len(secretword)):
            if secretword[i] not in correctletters:
                found = False
                break

        if found:
            print('You won the game ')
            print('The secret word was -----> ' +secretword.upper())
            done = True
    else:
        missedletters = missedletters + guess
        if len(missedletters) == len(hangmanpics)-1 :
            display(hangmanpics,missedletters,correctletters,secretword)
            print('You have lost the game, the word was :' +secretword)
            done = True

    if done:
        if playagain():
            os.system('cls')
            words = Welcomenote()
            missedletters = ''
            correctletters = ''
            done = False
            secretword = getRandomword(words)
        else:
            break
        
        
            
                
            
    

