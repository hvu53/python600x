def recurPower(base,exp):
    if exp <=0:
        return 1
    elif exp%2 ==0:
        return recurPower(base*base,exp/2)
    else:
        return base*recurPower(base,exp-1)
