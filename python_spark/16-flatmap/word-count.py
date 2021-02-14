# word-count.py
# August 3, 2020
#
# Count the number of occurrences of each word in a text file.
# Using the 'Book' text file.


from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('word-count')
sc = SparkContext(conf = conf)

lines = sc.textFile('Book')
words = lines.flatMap(lambda x: x.split())
words = words.map(lambda x: (x,1))
#totals = words.countByKey()
results = words.countByKey()
#results = totals.collect() #?

#for result in results:
#    cleanWord = result[0].encode('ascii', 'ignore')

#"""
for word, count in results.items():
    cleanWord = word.encode('ascii', 'ignore')
    if cleanWord:
        print cleanWord, count
#"""
"""
print results
"""
"""
for i in range(8):
    print results[i]
"""

sample = results.items()
#print sample
"""
for word in sample:
    cleanWord = word.encode('ascii', 'ignore')
    if cleanWord:
        print cleanWord
"""

for i in range(5):
    print results[i]


