# ratings-counter-test.py
# July 31, 2020
#
# Test of ratings-counter.py
# Used very small data set 'data.txt', prints out intermediate results, uses
# local data file

from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)

lines = sc.textFile("data.txt")
ratings = lines.map(lambda x: x.split()[2])
result = ratings.countByValue()
print(F"result:\n{result}")

sortedResults = collections.OrderedDict(sorted(result.items()))
for key, value in sortedResults.items():
    print("%s %i" % (key, value))
