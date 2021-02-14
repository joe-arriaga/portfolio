# popular-movies-dataframes.py
# August 9, 2020
#
# An updated version of an older script using DataFrames instead of RDDs. Find
# the most popular movies from the MovieLens ml-100k data set.


from pyspark.sql import SparkSession, Row, functions #SQL functions


def loadMovieNames():
    """Map of movieIDs to movie names. Used to create human-readable output."""
    movieNames = {}
    with open('../data/ml-100k/u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

spark = SparkSession.builder.appName("PopularMoviesDataFrames").getOrCreate()

# Load movie IDs into dictionary
nameDict = loadMovieNames()

# Get the raw data 
# Can use functions like spark.read.json() to convert directly to DataFrame
lines = spark.sparkContext.textFile("../data/ml-100k/u.data")
# Convert to RDD of Row objects
movies = lines.map(lambda x: Row(movieID = int(x.split()[1]) )) # only want to see how many times each movie was rated
# Convert that to a DataFrame
movieDataset = spark.createDataFrame(movies)

# Some SQL-style functions to sort all movies by popularity in one line!
topMovieIDs = movieDataset.groupBy("movieID").count().orderBy("count", ascending=False).cache()

# Show current results
# | movieID | count |
# +---------+-------+
# |     123 +    123|
# |     123 +    123|
# |     ... +    ...|
topMovieIDs.show()

# Take top 10 movies
top10 = topMovieIDs.take(10)

# Print results
print("\n")
for result in top10:
    print ("%s: %d") % (nameDict[result[0]], result[1])


# Stop the session
spark.stop()

