x = 25
epsilon = 0.01
stepSize = epsilon **2
numGuesses = 0
ans = 0.0

while abs(ans**2-x) >= epsilon and ans <x:
    ans += stepSize
    numGuesses +=1
print (str(numGuesses) + ' number of guesses')

if abs(ans**2-x) >= epsilon:
    print 'Failed on finding square root of  ' +str(x)
else:
    print('square root of  ' + str(x) + ' is ' + str(ans))
