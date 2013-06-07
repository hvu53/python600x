def oddTuples(aTup):
    index = 0
    tup =()
    for i in range(0, len(aTup)):
        if i %2 ==0:
            tup += (aTup[i],)
    return tup
