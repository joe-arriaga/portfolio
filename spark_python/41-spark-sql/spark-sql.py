# spark-sql.py
# August 8, 2020
#
# Exploring the basics of Spark SQL.


from pyspark.sql import SparkSession, Row
import collections

# Create SparkSession
#spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("SparkSQL").getOrCreate() #Windows
spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

def mapper(line):
    fields = line.split(',')
    # Give structure to unstructured csv
    return Row( ID=int(fields[0]),
                name=fields[1].encode('utf-8'), 
                age=int(fields[2]),
                numFriends=int(fields[3])
            )

lines = spark.sparkContext.textFile('../data/fakefriends.csv')
people = lines.map(mapper)
 
# Infer the schema, and register the DataFrame as a table
schemaPeople = spark.createDataFrame(people).cache() # cache b/c we want to perform multiple operations
schemaPeople.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table
teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")
#   Notice you don't have to specify where to get the 'age' data, it is already defined

# The results of SQL queries are RDDs and support all normal RDD operations
#   Can be treated as RDDs or SQL objects?
print("RDD collect() and print:")
for teen in teenagers.collect(): # RDD
    print(teen)
print("\nSQL show():")
teenagers.show() # SQL

# We can also use functions instead of SQL queries
# Slightly more efficient(?)
print("\nSQL Functions:")
schemaPeople.groupBy("age").count().orderBy("age").show()


