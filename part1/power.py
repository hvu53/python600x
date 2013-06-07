
def iterativePower(x,p):
    result = 1
    for i in range(p):
        print('iterative ' + str(i) + ' ,result: ' + str(result))
        result = result * x
    return result
