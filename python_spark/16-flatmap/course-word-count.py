# course-word-count.py
# August 3, 2020
# 
# Solution script provided by course.
# Count the number of occurrences of each word in a text file.
# Using the 'Book' text file.


from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('word-count')
sc = SparkContext(conf = conf)

lines = sc.textFile('Book')
words = lines.flatMap(lambda x: x.split())
wordCounts = words.countByValue()

for word, count in wordCounts.items():
    cleanWord = word.encode('ascii', 'ignore')
    if cleanWord:
        print cleanWord, count

#print wordCounts

