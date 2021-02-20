# joins.py
# August 6, 2020
#
# Exploring the join operations available in Spark.


from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('JoinTest')
sc = SparkContext(conf = conf)


set1 = sc.parallelize( [('a', 1), ('b', 4)] )
set2 = sc.parallelize( [('a', 2), ('a', 3), ('b', 5), ('b', 7), ('c', 6)] )
set3 = sc.parallelize( [('a', 2), ('a', 3), ('a', 4), ('c', 9), ('c', 10), ('d', 11)] )

# The types of joins
# Outer joins retain keys which do not appear in the other table, filling in the
# gap with a 'None' value. Left Outer Join retains unmatched keys only from the
# first table (set2 in this case, meaning 'b' is unmatched). Right Outer Join
# retains unmatched keys only from the second table (set3, meaning 'd' is unmatched).
# Full Outer Join retains unmatched keys from both tables ('b' and 'd').
#
# The regular join does not retain unmatched keys.

join = sorted(set2.join(set3).collect())
print '\nregular join:'
print join

leftOuterJoin = sorted(set2.leftOuterJoin(set3).collect())
print '\nleftOuterJoin:'
print leftOuterJoin

rightOuterJoin = sorted(set2.rightOuterJoin(set3).collect())
print '\nrightOuterJoin:'
print rightOuterJoin

#out = set2.fullOuterJoin(set3).collect()
#ordered = sorted(out)
fOJ = sorted(set2.fullOuterJoin(set3).collect())
#print 'out:'
#print out
#print '\nOrdered:'
#print ordered
print '\nfullOuterJoin:'
print fOJ








