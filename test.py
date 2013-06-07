class Frob(object):
    def __init__(self, name):
        self.name = name
        self.before = None
        self.after = None
    def setBefore(self, before):
        self.before = before
    def setAfter(self, after):
        self.after = after
    def getBefore(self):
        return self.before
    def getAfter(self):
        return self.after
    def myName(self):
        return self.name

def insert(atMe, newFrob):
    """
    atMe: a Frob that is part of a doubly linked list
    newFrob:  a Frob with no links
    This procedure appropriately inserts newFrob into the linked list that atMe is a part of.    
    """
    #linkedlist = [atMe]
    beforeAtMe = atMe.getBefore
    afterAtMe = atMe.getAfter
    if atMe.name <= newFrob.name:
        #linkedlist.append(newFrob)
        newFrob.setBefore(atMe)
    else:
        #linkedlist.prepend(newFrob)
        newFrob.setAfter(atMe)
    return newFrob
    if beforeAtMe == newFrob:
        newFrob.setAfter(atMe)
    elif afterAtMe == newFrob:
        newFrob.setBefore(atMe)

eric = Frob('eric')
andrew = Frob('andrew')
ruth = Frob('ruth')
fred = Frob('fred')
martha = Frob('martha')


insert(eric, ruth)
insert(eric, fred)
insert(ruth, martha)
