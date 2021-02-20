# popular-movie-names.py
# Auust 4, 2020
#
# Sort the MovieLens database by popularity. Which movie was watched most often?
# That is, which movie(ID) appears most often in the data set?
#
# Then broadcast the movie titles table to replace the movieID with its title.

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('PopularMovieNames')
sc = SparkContext(conf = conf)

def loadMovieNames():
    movieNames = {}
    with open('../data/ml-100k/u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

nameDict = sc.broadcast(loadMovieNames())

# Data format: UserID MovieID Rating Timestamp
lines = sc.textFile('../data/ml-100k/u.data')
parsedLines = lines.map(lambda x: (int(x.split()[1]), 1))
countedMovies = parsedLines.reduceByKey(lambda x,y: x + y)

sortedMovies = countedMovies.sortBy(lambda x: x[1])
#sortedMovies = countedMovies.sortBy(lambda x: x[1], ascending=False)
namedMovies = sortedMovies.map(lambda (name, count): (nameDict.value[name], count))
#namedMovies = sortedMovies.map(lambda x: (nameDict.value[x[0]], x[1]))

results = namedMovies.collect()

for result in results:
    print result

