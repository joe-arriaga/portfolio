# solution-most-popular-superhero2.py
# August 5, 2020
#
# Find the superhero which appears with the most other characters in the 
# 'Marvel+Graph' data set.


from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('MostPopularSuperhero')
sc = SparkContext(conf = conf)

def countCoOccurrences(line):
    elements = line.split()
    return (int(elements[0]), len(elements) - 1) # (ID, numFriends)

def parseNames(line):
    fields = line.split('\"')
    return (int(fields[0]), fields[1].encode('utf8')) # (ID, name)


names = sc.textFile('../data/Marvel+Names')
namesRdd = names.map(parseNames) # (ID, name)

# Initialize the count for each hero to 0
lines = sc.textFile('../data/Marvel+Graph')

pairings = lines.map(countCoOccurrences) # (ID, numFriends)
totalFriendsByCharacter = pairings.reduceByKey(lambda x,y: x + y) # (ID, totalFriends)

sortedHeros = totalFriendsByCharacter.sortBy(lambda x: x[1]) # (ID, totalFriends)

#mostPopularName = namesRdd.lookup(mostPopular[1])[0]
namedHeros = sortedHeros.join(namesRdd) # (ID, (numFriends, name))
flat = namedHeros.map(lambda (ID, (friends, name)): (friends, name, ID))
flat = flat.sortBy(lambda x: x[0])



#print mostPopularName + ', ' + str(mostPopular[0]) + ' friends'

#results = sortedHeros.collect()
#results = namedHeros.collect()
results = flat.collect()
for result in results:
    print result

