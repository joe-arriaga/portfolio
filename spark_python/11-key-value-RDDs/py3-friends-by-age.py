from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("FriendsByAge")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    age = int(fields[2])
    numFriends = int(fields[3])
    return (age, numFriends)

lines = sc.textFile("fakefriends.csv")
rdd = lines.map(parseLine)

# mapValues - adds an instance marker; could count # of instances a different way, but this is pretty efficient (prevents having to deal with another variable)
#   eg. (33, 385) => (33, (385, 1))
#       (33, 2)   => (33, (2, 1))

# reduceByKey - for each key, combine num_friends 1st element and num_instances 2nd element of all instances
#   updates value, maintains key
#   eg. (33, (385, 1)) and (33, (2, 1)) => (33, (387, 2))
totalsByAge = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
#averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
averagesByAge = totalsByAge.mapValues(lambda x: (x[0] / x[1], x[1])) # x[1] is # of instances
results = averagesByAge.sortByKey().collect()
#results = collections.OrderedDict(sorted(averagesByAge.items())) # sort by key, create dict
for result in results:
    #print(result)

    print(F"age {result[0]}: avg = {result[1][0]:6.3f},   {result[1][1]:2} instances")
    #print(F"age: {result[0]}", end=' ')
    #print(F"friends: {result[1][0]}", end=' ')
    #print(F"instances: {result[1][1]}")

