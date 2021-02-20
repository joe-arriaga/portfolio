# movie-similarities-1m-local-data.py
# August 7, 2020
#
# Modified the original script to make use of partitioning to run on a cluster
# on the MovieLens 1 million item data set.
# Use Item-Based Collaborative Filtering to determine similarities between movies
# for the purpose of making recommendations.
#
# ----Input Argument = 260 (Star Wars)----
# ---spark-submit --conf "spark.ui.showConsoleProgress=True" movie-similarities.py 50---
# spark-submit --executor-memory 1g movie-similarities-1m.py 260

import sys
from pyspark import SparkConf, SparkContext
from math import sqrt


def loadMovieNames():
    movieNames = {}
    with open ('../data/ml-1m/movies.dat') as f:
        for line in f:
            fields = line.split('::')
            movieNames[int(fields[0])] = fields[1].decode('ascii', 'ignore')
    return movieNames

def makePairs( (user, ratings) ):
    (movie1, rating1) = ratings[0]
    (movie2, rating2) = ratings[1]
    return ((movie1, movie2), (rating1, rating2))

def filterDuplicates( (userID, ratings) ):
    """Enforces monotonic ordering of movie pairs. Eliminates different ordering
    of the same pair, and pairs of the same movie.
    """
    (movie1, rating1) = ratings[0]
    (movie2, rating2) = ratings[1]
    return movie1 < movie2

def computeCosineSimilarity(ratingPairs):
    numPairs = 0
    sum_xx = sum_yy = sum_xy = 0
    for ratingX, ratingY in ratingPairs:
        sum_xx += ratingX * ratingX
        sum_yy += ratingY * ratingY
        sum_xy += ratingX * ratingY
        numPairs += 1

    numerator = sum_xy
    denominator = sqrt(sum_xx) * sqrt(sum_yy)

    score = 0
    if denominator:
        score = numerator / (float(denominator))

    return (score, numPairs)


conf = SparkConf() # pass master node? and app name on command line
sc = SparkContext(conf = conf)

print "\nLoading movie names..."
nameDict = loadMovieNames()

# data starts as: userID movieID rating timestamp
# Map input ratings to: (userID, (movieID, rating))
# I could only get it to work if the data was in HDFS, not local on the master node
data = sc.textFile('/user/sysadmin/data/ml-1m/u.data')
ratings = data.map(lambda l: l.split("::")).map(lambda l: ( int(l[0]), (int(l[1]), float(l[2])) ) )

# Find every pair of movies rated by the same user
#   self-join
ratingsPartitioned = ratings.partitionBy(100)
joinedratingsPartitioned = ratings.join(ratings) # (userID, ((movieID, rating), (movieID, rating)))

# Filter out duplicate pairs (and pairs of same movie)
# (userID, ((movieID, rating), (movieID, rating)))
uniqueJoinedRatings = joinedRatings.filter(filterDuplicates) 

# Make the movie pairs the key (don't care about user): 
#       ((movieID1, movieID2), (rating1, rating2))
moviePairs = uniqueJoinedRatings.map(makePairs)

# GroupByKey() to get every rating pair for each movie pair
#       ( (movie1, movie2), [(rating1, rating2), (rating1, rating2), (rating1, rating2), ...] )
moviePairRatings = moviePairs.groupByKey()

# Compute similarity between ratings
# cache - allows us to use moviePairSimilarites multiple times w/o recomputing
#       ( (movie1, movie2), (similarityScore, numPairsEvaluated) )
moviePairSimilarities = moviePairRatings.mapValues(computeCosineSimilarity).cache()

### Sort, save, and display results
# Save results if desired
#moviePairSimilarities.sortByKey()
# Will get one file per executor (core)
#moviePairSimilarites.saveAsTextFile("movie-similarity.txt")

# Extract only similar results to the movie of interest provided as an argument
if len(sys.argv) > 1:
    scoreThreshold = 0.97
    coOccurrenceThreshold = 50

    movieID = int(sys.argv[1])

    # Filter for good movies similar to our movie of interest
    # pair must contain our movie, must be similar, and have many people who rated both
    filteredResults = moviePairSimilarities.filter(lambda (pair,sim): \
            (pair[0] == movieID or pair[1] == movieID) \
            and sim[0] > scoreThreshold and sim[1] > coOccurrenceThreshold) 

    # Sort by quality score
    results = filteredResults.map(lambda (pair,sim): (sim,pair)).\
            sortByKey(ascending = False).take(10)
    #results = filteredResults.sortBy(lambda x: x[1], ascending=False).take(10)
    #results = filteredResults.sortBy(lambda (pair,sim): sim, ascending=False).take(10)

    print "Top 10 similar movies for " + nameDict[movieID]
    for result in results:
        (sim, pair) = result
        #(pair, sim) = result
        # Display movie similar to our movie of interest
        similarMovieID = pair[0]
        if similarMovieID == movieID:
            similarMovieID = pair[1]
        print nameDict[similarMovieID] + "\tscore: " + str(sim[0]) + "\tstrength: " + str(sim[1])





