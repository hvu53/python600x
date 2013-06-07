eps = 0.01
k = 24.0
guess = k/2.0

while abs(guess**2-k) >= eps:
    guess = guess - ((guess**2 - k)/(2*guess))
    print guess
print ('guess is ' + str(guess))
