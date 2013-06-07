def fibMetered(x):
    global numCalls
    numCalls += 1
    if x == 0 or x ==1:
        return 1
    else:
        return fibMetered(x-1) + fibMetered(x-2)

def test(n):
    for i in range(n+1):
        global numCalls
        numCalls =0
        print('fib of ' + str(i) + ' is' + str(fibMetered(i)))
        print ('numCalls is ' + str(numCalls))
