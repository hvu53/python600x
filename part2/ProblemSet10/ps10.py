# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 
# use weightedgraph with edges is the weight of total distance and totaloutdoordistance

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    
    f = open(mapFilename, 'r', 0)
    g = WeightedDigraph()

    for line in f.readlines():
        src, dest, tdist, odist = line.split()
        
        node1 = Node(src)
        node2 = Node(dest)
        if node1 not in g.nodes:
            g.addNode(node1)
        if node2 not in g.nodes:
            g.addNode(node2)
        edge = WeightedEdge(node1,node2,tdist,odist)
        g.addEdge(edge)

    return g    
       


#
# 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def findDistances(digraph, path): #helper function
        """
        Finds the total distance and outdoor distance of a path.

        Assumes that the path is a list of valid nodes.

        Returns a tuple of the total distance and outdoor distance
        """
        total_distance = 0
        outdoor_distance = 0
        for node in range(len(path)-1): #for each node of the path except for the last one
            for dest in digraph.edges[Node(path[node])]: #for each destination of a node
                if dest[0] == Node(path[node+1]): #if destination is the next node in path
                    total_distance += int(dest[1][0]) #add the total distance
                    outdoor_distance += int(dest[1][1])
        return (total_distance, outdoor_distance)

    
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    def bruteForceSearchHelper(digraph, start, end, maxTotalDist, maxDistOutdoors, path = []):
        #helper function
        path = path[:]
        path += [start]
        paths = [path]
        if start == end:
            return paths
        for node in digraph.childrenOf(Node(start)):
            if repr(node) not in path: #avoid cycles
                new_paths = bruteForceSearchHelper(digraph,repr(node),end,maxTotalDist, maxDistOutdoors, path)
                for a_path in new_paths:
                    paths.append(a_path) #append new paths
        for a_path in paths[:]:
            if a_path[-1] != end: #remove invalid paths
                paths.remove(a_path)
        return paths

    #outside helper functions
    paths = bruteForceSearchHelper(digraph, start, end, maxTotalDist, maxDistOutdoors)
    #choosing the shortest path
    min_total_dist = None
    shortest = None
    for path in paths:
        total_dist, outdoor_dist = findDistances(digraph, path)
        if total_dist <= maxTotalDist and outdoor_dist <= maxDistOutdoors\
            and (shortest == None or total_dist < min_total_dist): #if shortest valid path found
            shortest = path[:]
            min_total_dist = total_dist
    if shortest == None:
        raise ValueError("no such path exists")
    return [str(i) for i in shortest]

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    start = Node(start)
    end = Node(end)
    best_path = None
    best_path_total_distance = maxTotalDist
    paths = directedPaths(digraph,start,end,maxTotalDist,maxDistOutdoors,best_path_total_distance)
    for path in range(len(paths)):
        path_distances = pathDistances(digraph, paths[path])
        if (path_distances[0]<=maxTotalDist and path_distances[0]<=best_path_total_distance and path_distances[1]<=maxDistOutdoors):
            best_path = paths[path]
            best_path_total_distance = path_distances[0]
    if best_path!=None:
        answer = []
        for node in best_path:
            answer.append(str(node))
        return answer
    else:
        raise ValueError('no paths satisfy constraints')



def directedPaths(digraph, start, end, maxTotalDist, maxDistOutdoors, best_path_total_distance, path = []):

    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in digraph.childrenOf(start):
        if node not in path and pathDistances(digraph,path)[0]<=best_path_total_distance:
            best_path_total_distance=pathDistances(digraph,path)
            newpaths = directedPaths(digraph,node,end, maxTotalDist,maxDistOutdoors,best_path_total_distance,path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths



def pathDistances(digraph, testpath):
    """
    takes a digraph with weighted paths(total and outdoors) and returns a tuple
    with total distance at index 0 and outdoor distance at index 1
    """
    total_distance=0
    total_outdoor_distance=0
    for n in range(len(testpath)-1):
        testedges=digraph.edges[testpath[n]]
        if len(testedges)==1:
            total_distance+=float(testedges[0][1][0])
            total_outdoor_distance+=float(testedges[0][1][1])
        else:
            for testedge in testedges:
                if testedge[0]==testpath[n+1]:
                    total_distance+=float(testedge[1][0])
                    total_outdoor_distance+=float(testedge[1][1])
    return (total_distance,total_outdoor_distance)

# Test Case
#### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     Test cases
#     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     print 'nodes', mitMap.nodes
#     print 'edges', mitMap.edges


#     LARGE_DIST = 1000000

#     Test case 1
#     print "---------------"
#     print "Test case 1:"
#     print "Find the shortest-path from Building 32 to 56"
#     expectedPath1 = ['32', '56']
#     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath1
#     print "Brute-force: ", brutePath1
#     print "DFS: ", dfsPath1
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
#     print "---------------"
#     print "Test case 2:"
#     print "Find the shortest-path from Building 32 to 56 without going outdoors"
#     expectedPath2 = ['32', '36', '26', '16', '56']
#     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
#     print "Expected: ", expectedPath2
#     print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr
