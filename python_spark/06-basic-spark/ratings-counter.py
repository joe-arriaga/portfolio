# ratings-counter.py

from pyspark import SparkConf, SparkContext
import collections

# define how Spark will run
conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf) # pass configuration settings to SparkContext

#lines = sc.textFile("file:///SparkCourse/ml-100k/u.data")
lines = sc.textFile("ml-100k/u.data") # load data
# !!! Must assign result to new variable !!!
# operations are not done in-place. why?
ratings = lines.map(lambda x: x.split()[2]) # grab each line and extract 3rd value

#------------------- RDD^^, Python objects \/\/ -------------------------

result = ratings.countByValue() # count # of each value, !! returns a Python object, not RDD !!

sortedResults = collections.OrderedDict(sorted(result.items())) # sort by key, create dict
for key, value in sortedResults.items(): # print ordered dict
    print("%s %i" % (key, value))
