# dstream.py
# August 9, 2020
#
# Example from the Spark SDK
# Example of using the Dstream object for Spark Streaming.
# Counts how often each word appears in the files in the 'books' directory,
# updates every one second.


from pyspark import SparkConf, SparkContext

conf = SparkConf.setMaster('local[*]').setAppName('DStreamWordCount')
sc = SparkContext(conf = conf)


ssc = Streamingcontext(sc, 1) # Update every one second
lines = ssc.textFileStream('books')
counts = lines.flatMap(lambda line: line.split(' '))\
        .map(lambda x: (x, 1)\
        .reduceByKey(lambda a, b: a + b)
counts.pprint()


ssc.start()
ssc.awaitTermination()

