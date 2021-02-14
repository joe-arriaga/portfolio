# min-temps.py
# August 2, 2020

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('min-temperatures')
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',') 
    stationID = fields[0]
    entryType = fields[2]
    temperature = (float(fields[3]) / 10) * (9.0/5.0) + 32
    return (stationID, entryType, temperature)

lines = sc.textFile('1800.csv')
parsedLines = lines.map(parseLine)
minTemps = parsedLines.filter(lambda x: 'TMIN' in x[1])
stationTemps = minTemps.map(lambda x: (x[0], x[2]))
minTemps = stationTemps.reduceByKey(lambda x, y: min(x,y))
results = minTemps.collect()

for result in results:
    print result[0] + '\t{:.2f}F'.format(result[1])
