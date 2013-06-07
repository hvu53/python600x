class intSet(object):
    """An intSet is a set of integers
    The value is represented by a list of ints, self.vals.
    Each int in the set occurs in self.vals exactly once."""

    def __init__(self):
        """Create an empty set of integers"""
        self.vals = []

    def insert(self, e):
        """Assumes e is an integer and inserts e into self""" 
        if not e in self.vals:
            self.vals.append(e)

    def member(self, e):
        """Assumes e is an integer
           Returns True if e is in self, and False otherwise"""
        return e in self.vals

    def remove(self, e):
        """Assumes e is an integer and removes e from self
           Raises ValueError if e is not in self"""
        try:
            self.vals.remove(e)
        except:
            raise ValueError(str(e) + ' not found')

    def __str__(self):
        """Returns a string representation of self"""
        self.vals.sort()
        return '{' + ','.join([str(e) for e in self.vals]) + '}'

###############

class hashSet():
    def __init__(self, numBuckets): 
        '''
        numBuckets: int. The number of buckets this hash set will have. 
        Raises ValueError if this value is not an integer, or if it is not greater than zero.

        Sets up an empty hash set with numBuckets number of buckets.
        '''
        if type(numBuckets) != int: 
            raise ValueError(str(numBuckets) + ' must be an integer')
        if numBuckets <= 0:
            raise ValueError(str(numBuckets) + ' must be greater than zero')
        self.numBuckets = numBuckets
        self.hashSet = []
        for b in range(numBuckets):
            self.hashSet.append([])
            
    def hashValue(self, e):
        '''
        e: an integer

        returns: a hash value for e, which is simply e modulo the number of 
         buckets in this hash set. Raises ValueError if e is not an integer.
        '''
        if type(e) != int:
            raise ValueError(str(e) + ' must be an integer')
        return e % self.getNumBuckets()

    def member(self, e):
        '''
        e: an integer
        Returns True if e is in self, and False otherwise. Raises ValueError if e is not an integer.
        '''
        bucket = self.hashValue(e)
        return e in self.hashSet[bucket]
        

    def insert(self, e):
        '''
        e: an integer
        Inserts e into the appropriate hash bucket. Raises ValueError if e is not an integer.
        '''
        if not self.member(e):
            bucket = self.hashValue(e)
            self.hashSet[bucket].append(e)
            
    def remove(self, e):
        '''
        e: is an integer 
        Removes e from self
        Raises ValueError if e is not in self or if e is not an integer.
        '''
        bucket = self.hashValue(e)
        try:
            self.hashSet[bucket].remove(e)
        except:
            raise ValueError(str(e) + ' not found')