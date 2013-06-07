class Queue(object):

    def __init__(self):
        "Initializes 1 attribute: a list to keep track of the queue's elements"
        self.qlist = []

    def insert(self, element):
        "Adds an element to the attribute list using append"
        self.qlist.append(element)

    def remove(self):
        "Removes an element from the attribute list"
        # Check if the list is empty; if so then raise a ValueError
        if self.qlist == []:
            raise ValueError()
        else:
            # Otherwise we want to remove the first element from the list
            # and return that to the user.
            element = self.qlist[0]
            self.qlist.remove(element)
            return element
            # Could also do this in 1 line:
            # return self.qlist.pop(0)
