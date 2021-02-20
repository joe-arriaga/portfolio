# movie-recommendations-als.y
# August 9, 2020
#
# Use Alternating Least Squares model from MLLib to produce movie recommendations
# from the MovieLens ml-100k data set. Pass in the userID to create recommendations
# for as an argument.
#
# Data format is: userID movieID rating timestamp
#
# Edited ml-100k/u.data to add custom test user so we can judge appropriateness
# of recommendations. This allows us to judge the success of the algorithm.
# Test user is user 0 at top of file. 
# Star Wars: A New Hope (50) = 5 stars,
# Star Wars: Empire Strikes Back (172) = 5 stars, 
# Gone With the Wind (133) = 1 star.
#
# Doesn't work. Gets different results on each run.
# Potential Reasons:
# - model may be sampling rather than using all data
# - model may not be well trained
#   - algorithm parameters may not be tuned well for this problem (many are left
#       as default)
# - model may be overfitting / falling into local maxima?
# - ALS() function is a black box
#   - How do we know it is implemented correctly?
#
# Small problems in algorithms result in large errors
# Quality of input data can create bad results


import sys
from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS, Rating


def loadMovieNames():
    movieNames = {}
    with open("../data/ml-100k/u.item") as f:
    #with open("../data/ml-100k/u.item", encoding='ascii', errors='ignore') as f:
        for line in f:
            fields = line.split("|")
            movieNames[int(fields[0])] = fields[1].decode('ascii', 'ignore')
            #movieNames[int(fields[0])] = fields[1]
    return movieNames


conf = SparkConf().setMaster('local[*]').setAppName("MovieRecommendationsALS")
sc = SparkContext(conf = conf)

print "\nLoading movie names..."
nameDict = loadMovieNames()

data = sc.textFile("../data/ml-100k/u.data")

ratings = data.map(lambda l: l.split())\
        .map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2]) ))\
        .cache()

# Build the recommendation model using Alternative Least Squares
print "\nTraining recommendation model..."
rank = 10
numIterations = 6 # local machine dies if too high; 10 is OK, 20 is too much
# creates recommendation profiles for all users
model = ALS.train(ratings, rank, numIterations)

userID = int(sys.argv[1])

# Show previous ratings for user
print"\nRatings for user ID " + str(userID) + ":"
userRatings = ratings.filter(lambda l: l[0] == userID)
for ratings in userRatings.collect():
    print nameDict[int(ratings[1])] + ": " + str(ratings[2])

# show recommendations for user of interest
print "\nTop 10 recommendations:"
recommendations = model.recommendProducts(userID, 10)
for recommendation in recommendations:
    print nameDict[int(recommendation[1])] + ", score: " + str(recommendation[2])


