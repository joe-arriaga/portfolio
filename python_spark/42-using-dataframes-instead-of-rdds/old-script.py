# old-script.py (most-popular-movie.py)
# Auust 4, 2020
#
# Old script using RDDs to compare to new version using DataFrames.
#
# Sort the MovieLens database by popularity. Which movie was watched most often?
# That is, which movie(ID) appears most often in the data set?

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('MoviePopularity')
sc = SparkContext(conf = conf)

def parseLines(line):
    fields = line.split()
    return (int(fields[1]), 1)

# Data format: UserID MovieID Rating Timestamp
lines = sc.textFile('../data/ml-100k/u.data')
parsedLines = lines.map(parseLines)
countedMovies = parsedLines.reduceByKey(lambda x,y: x + y)

sortedMovies = countedMovies.sortBy(lambda x: x[1])
#sortedMovies = countedMovies.sortBy(lambda x: x[1], ascending=False)

results = sortedMovies.collect()

for result in results:
    print result

