def genPrimes():
    primes = []
    last = 1
    while True:
        last +=1
        for i in primes:
            if (last %i) ==0:
                break
        else:
            primes.append(last)
            yield last
