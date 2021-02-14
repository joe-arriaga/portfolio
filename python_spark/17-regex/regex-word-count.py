# course-word-count.py
# August 3, 2020
# 
# Solution script provided by course.
# Count the number of occurrences of each word in a text file.
# Using the 'Book' text file.


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
wordCounts = words.countByValue()

for word, count in wordCounts.items():
    cleanWord = word.encode('ascii', 'ignore')
    if cleanWord:
        print cleanWord, count


