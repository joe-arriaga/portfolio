# ordered-word-count.py
# August 3, 2020
# 
# Solution script provided by course.
# Count the number of occurrences of each word in a text file.
# Using the 'Book' text file.
#
# This script follows the solution provided in the course and flips the key-value
# pair to be (cumulative_total, word) and then uses the sortByKey() function.
# The other script, ordered-word-count2.py, leaves the cumulative occurrences of
# each word in the value portion of the key-value pair and uses a technique to
# order based on value.

import re
from pyspark import SparkConf, SparkContext

def normalizeWords(text):
    """compile() breaks up text into words (discards punctuation).
    lower() negates differences caused by capitalization.
    """
    return re.compile(r'\W+', re.UNICODE).split(text.lower())

conf = SparkConf().setMaster('local').setAppName('word-count')
sc = SparkContext(conf = conf)

lines = sc.textFile('../16/Book')
words = lines.flatMap(normalizeWords)

words = words.map(lambda x: (x,1))
wordCounts = words.reduceByKey(lambda x, y: x + y)
countedWords = wordCounts.map(lambda (x,y): (y,x))
sortedWords = countedWords.sortByKey()

results = sortedWords.collect()

#"""
for result in results:
    count = str(result[0])
    word = result[1].encode('ascii', 'ignore')
    if word:
        print word + '\t' + count
#"""
"""
for count, word in results:
    cleanWord = word.encode('ascii', 'ignore')
    if cleanWord:
        print cleanWord, count
"""

#print results

