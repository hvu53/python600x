items = [1,2,3]
def ps1(items):
    N = len(items)
    for i in xrange(2**N):
        combo = []
        for j in xrange(N):
            if (i >> j) % 2 == 1:
                combo.append(items[j])
        yield combo

def ps2(items):
    x = len(items)
    for i in range(1 << x):
        print [items[j] for j in range(x) if (i & (1 << j))]
               
def ps_rec(items):
    if items:
        first, rest = items[:1], items[1:]
        for portion in ps2(rest):
            yield portion
            yield first + portion
    else:
        yield []
from itertools import combinations
###
l = ["x", "y", "z", ]
def ps3(items):
    combo = []
    for r in range(len(items) + 1):
        #use a list to coerce a actual list from the combinations generator
        combo.append(list(combinations(items,r)))
    return combo

l_powerset = ps3(l)

for i, item in enumerate(l_powerset):
    print "All sets of length ", i
    print item

 ####   
def ps_itertls(items):
    "itertools recipe (returns tuples)"
    return chain.from_iterable(combinations(items, r) for r in range(len(items)+1))

def ps_iterlist(items):
    "itertools variant returning lists"
    for r in range(len(items) +1):
        for combination in list(combinations(items.r)):
            yield list(combination)

def list_powerset(items):
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in items:
        # for every additional element in our set
        # the power set consists of the subsets that don't
        # contain this element (just take the previous power set)
        # plus the subsets that do contain the element (use list
        # comprehension to add [x] onto everything in the
        # previous power set)
        result.extend([subset + [x] for subset in result])
    return result
 
# the above function in one statement
def list_powerset2(items):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  items, [[]])
 
def ps4(items):
    return frozenset(map(frozenset, list_powerset(list(items))))

def yieldAllCombos(items):
    """
    Generates all combinations of N items into two bags, whereby each item is in one or zero bags.

    Yields a tuple, (bag1, bag2), where each bag is represented as a list of which item(s) are in each bag.
    """
    # Your code here
    N = len(items)
    for i in xrange(3**N):
        bag1 = []
        bag2 = []
        for j in xrange(N):
            if (i / (3**j)) %3 ==1:
                bag1.append(items[j])
            elif (i/ (3**j)) % 3 ==2:
                bag2.append(items[j])
                
        return (bag1,bag2)
