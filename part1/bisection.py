x = 25
epsilon = 0.01
numGuess = 0
low = 0.0
high = x
ans = (low+high)/2

while abs(ans**2-x) >= epsilon:
    print('low: ' + str(low) + ', high: ' + str(high) + ', ans: ' + str(ans))
    numGuess +=1
    if ans**2 > x:
        high = ans
    else:
        low = ans
    ans = (low+high)/2
print('number of guess ' + str(numGuess))
print('answer is ' + str(ans))
