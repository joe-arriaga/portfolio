# structured-streaming.py
# August 9, 2020
#
# Monitors directory of web server access logs, count number of each status code.
#
# Running the Script:
# 1. You will need two terminal sessions.
# 2. In one terminal, start the spark job with 'spark-submit structured-streaming.py'
# 3. In the other terminal, copy the 'access-logs.txt' file into the 'logs' directory
#    3.1 The script should print output to the console
# 4. You can copy the access logs file to the 'logs' directory multiple times to see
#    it handle the stream, just be sure to give each destination file a different name.
#    4.1 Each time you copy the file the 'count' values should go up by the same amount
#        since the same data is being fed in.
# 5. When you are done, terminate with ^C.


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession

from pyspark.sql.functions import regexp_extract


# Create SparkSession
spark = SparkSession.builder.appName("StructuredStreaming").getOrCreate()

# Monitor the 'logs' directory for new log data
# read in the raw lines to accessLines
accessLines = spark.readStream.text("logs")
#   accessLines = spark.read.text("logs") ?would allow you to use a static DF, (for development)

# Parse out the common log format to a DataFrame
contentSizeExp = r'\s(\d+)$'
statusExp = r'\s(\d{3})\s'
generalExp = r'\"(\S+)\s(\S+)\s*(\S*)\"'
timeExp = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})]'
hostExp = r'(^\S+\.[\S+\.]+\S+)\s'

# Extracted values become values in columns of alias
logsDF = accessLines.select(regexp_extract('value', hostExp, 1).alias('host'),
                            regexp_extract('value', timeExp, 1).alias('timestamp'),
                            regexp_extract('value', generalExp, 1).alias('method'),
                            regexp_extract('value', generalExp, 2).alias('endpoint'),
                            regexp_extract('value', generalExp, 3).alias('protocol'),
                            regexp_extract('value', statusExp, 1).cast('integer').alias('status'),
                            regexp_extract('value', contentSizeExp, 1).cast('integer').alias('content_size'))

# Keep running count of every access by status code
statusCountsDF = logsDF.groupBy(logsDF.status).count()

# Start streaming query, write results to console
query = ( statusCountsDF.writeStream.outputMode("complete").format("console").queryName("counts").start() )

# Run forever until terminated
query.awaitTermination()

# Cleanly shut down SparkSession
spark.stop()

