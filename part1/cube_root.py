x = float(raw_input(enter fractions: ))
p = 0
while ((2**p)*x) %1 != 0:
    print ('remainder =' + str((2**p)*x - int((2**p)*x)))
    p += 1

num = int(x*(2**p))
result = ""
if num =0:
    return '0'
while num >0:
    result = str(num%2) + result
    num = num/2
 
for i in range(p-len(result)):
    result = '0' + result

esult = result[0:-p] + '.' + result[-p:]
print('The result is ' + str(x)
