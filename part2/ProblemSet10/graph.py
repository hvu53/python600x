# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedEdge(Edge):
    def __init__(self, src, dest, tcost, ocost):
        self.src = src
        self.dest = dest
        self.tcost = tcost
        self.ocost = ocost
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def getTotalDistance(self):
        return self.tcost
    def getOutdoorDistance(self):
        return self.ocost
    def __str__(self):
        return '{0}->{1} ({2}, {3})'.format(self.src, self.dest, self.tcost,self.ocost)
    
class WeightedDigraph(Digraph):
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        tcost = float(edge.getTotalDistance())
        ocost = float(edge.getOutdoorDistance())
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest,(tcost,ocost)])
        
    def childrenOf(self, node):
        nodeL = []
        for i in self.edges[node]:
            nodeL.append(i[0])
        return nodeL
    
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2} {3}\n'.format(res, k, d[0],d[1])
        return res[:-1]
    
def test():
    g = WeightedDigraph()
    nh = Node('h')
    nj = Node('j')
    nk = Node('k')
    nm = Node('m')
    ng = Node('g')
    e1 = WeightedEdge(nh, nk,84, 47)
    e2 = WeightedEdge(nm, nj, 40, 8)
    e3 = WeightedEdge(nm, nh, 38, 15)
    e4 = WeightedEdge(nm, nk, 58, 29)
    e5 = WeightedEdge(nh, nj, 37, 6)
    e6 = WeightedEdge(nk, nm, 25, 6)
    e7 = WeightedEdge(nk, nm, 30, 23)
    e8 = WeightedEdge(nk, nm, 91, 22)
    g.addNode(nh)
    g.addNode(nj)
    g.addNode(nk)
    g.addNode(nm)
    g.addNode(ng)
    g.addEdge(e1)
    g.addEdge(e2)
    g.addEdge(e3)
    g.addEdge(e4)
    g.addEdge(e5)
    g.addEdge(e6)
    g.addEdge(e7)
    g.addEdge(e8)
    print g
    print g.childrenOf(nh)
    
