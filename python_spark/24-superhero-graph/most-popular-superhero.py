# most-popular-superhero.py
# August 5, 2020
#
# Find the superhero which appears with the most other characters in the 
# 'Marvel+Graph' data set.


from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('MostPopularSuperhero')
sc = SparkContext(conf = conf)

def getCharacterNames():
    namesDict = {}
    with open('../data/Marvel+Names') as f:
        for line in f:
            fields = line.split()
            namesDict[fields[0]] = fields[1]
    return namesDict

def parseLines(line):
    fields = line.split()
    return (int(fields[0]), fields[1]) # (ID, name)

def countFriends():
    friendsDict = {}
    with open('../data/Marvel+Graph') as f:
        for line in f:
            fields = line.split()
            friendsDict[int(fields[0])] = len(fields) - 1
    return friendsDict


namesDict = sc.broadcast(getCharacterNames)

########### DELETE ##########
# \/\/ This is bad because it creates a Python object, we want to work with an
# RDD because it is _much_ more efficient
#heros = ()
#for (ID,name) in namesDict.value#:
#    heros.append(int(ID), 0)
#heros = namesDict.value.map(lambda (ID, name): (int(ID), 0))
#################################

# Initialize the count for each hero to 0
lines = sc.textFile('../data/Marvel+Names')
heros = lines.map(parseLines).map(lambda (ID,name): (ID, 0))
#heros = lines.map(lambda line: (int(line.split()[0]), 0)) # heros = (ID, 0)

# Read through the graph and increment each hero for every time they appear in
# another hero's graph. The first entry of each line is the hero of interest and
# should not be counted.
# Can just subtract 1 from each character at end to account for their own graph?
#   OK if every character is guaranteed to have 1 and only 1 entry
numFriends = heros.map(countFriends)





results = heros.collect()
for result in results:
    print result


