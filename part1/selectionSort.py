def selSort(L):
    for i in range(len(L)-1):
        minInd = i
        minVal = L[i]
        j =i+1
        while j <len(L):
            if minVal > L[j]:
                minInd = j
                minVal = L[j]
            j+=1
        temp = L[i]
        L[i] = L[minInd]
        L[minInd] = temp
