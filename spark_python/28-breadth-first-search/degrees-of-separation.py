# degrees-of-separation.py
# August 5, 2020

# Use Breadth-First Search to find the minimum distance between two heros.
# Node states are: new, touched, explored

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('DegreesOfSeparation')
sc = SparkContext(conf = conf)

def convertToBFS(line):
    """Convert a line of raw data to an initialized node representation."""
    fields = line.split()
    heroID = int(fields[0])
    connections = []
    for connection in fields[1:]:
        connections.append(int(connection))
    state = 'new'
    distance = 9999

    if (heroID == startCharacterID):
        state = 'touched'
        distance = 0

    return (heroID, (connections, distance, state))

def createStartingRdd():
    inputFile = sc.textFile('../data/Marvel+Graph')
    return inputFile.map(convertToBFS)

# Mapper: Advance BFS - Create new nodes for each connection to a touched node, 
#           change state of nodes
def bfsMap(node):
    characterID = node[0]
    data = node[1]
    connections = data[0]
    distance = data[1]
    state = data[2]

    results = []

    if state == 'touched':
        for connection in connections:
            newCharacterID = connection
            newDistance = distance + 1
            newState = 'touched'
            if targetCharacterID == connection:
                foundTarget.add(1)

            newEntry = (newCharacterID, ([], newDistance, newState))
            results.append(newEntry)
        state = 'explored'

    results.append( (characterID, (connections, distance, state)) )
    return results

# Reducer: Combine all nodes for a given hero ID, preserve shortest distance and
#           most processed state, and list of connections on shortest path?
def bfsReduce(data1, data2):
    edges1 = data1[0]
    edges2 = data2[0]
    distance1 = data1[1]
    distance2 = data2[1]
    state1 = data1[2]
    state2 = data2[2]

    distance = 9999
    state = 'new'
    edges = []

    # If one of the nodes is the original(/a previous?) node, its connections
    # must be preserved
    if len(edges1) > 0:
        edges = edges1
    elif len(edges2) > 0:
        edges = edges2

    # Preserve minimum distance - finds least of all three distances
    if distance1 < distance:
        distance = distance1
    if distance2 < distance:
        distance = distance2

    # Preserve most explored state
    if state1 == 'new' and (state2 == 'touched' or state2 == 'explored'):
        state = state2
    if state1 == 'touched' and state2 == 'explored':
        state = state2

    return (edges, distance, state)


##### Main Program
startCharacterID = 5306 #SpiderMan
targetCharacterID = 14 #ADAM 3,031

# Accumulator, used to signal when we find the target character during
# BFS traversal
foundTarget = sc.accumulator(0)

iterationRdd = createStartingRdd()

for iteration in range(10): # Max 10 iterations/10 degrees of separation
    print 'Running BFS iteration# ' + str(iteration+1)

    # Create new vertices as needed to explore further or reduce distances in
    # the reduce stage.
    # If we encounter the target node as a 'touched' node, increment the
    # accumulator to signal that we're done.
    mapped = iterationRdd.flatMap(bfsMap)

    # Note that the mapped.count() action here forces the RDD to be evaluated,
    # and that causes the accumulator to be updated.
    print "Processing " + str(mapped.count()) + " values."

    if foundTarget.value > 0:
        print "Found the target character1 from " + str(foundTarget.value) \
                + " different direction(s)."
        break

    # Reducer combines data fro each character ID, preserving the most explored
    # state and the shortest path.
    #  - combines work of latest iteration
    iterationRdd = mapped.reduceByKey(bfsReduce)

