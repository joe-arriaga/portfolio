# amount-spent.py
# August 4, 2020
#
# USAGE: spark-submit amount-spent.py 'sortMethod'
#   'sortMethod' can be:
#       customerID - to sort by customer ID
#       total      - to sort by the total amount each customer spent
#
# Exercise: Find the total amount spent by each customer from the file
# 'customer-orders.csv'.
#
# Note: This script uses raw_input() in getSortMethod() which only works for
# Python 2. You can search the script for 'Python 2'


### Import Spark and Create context
from pyspark import SparkConf, SparkContext
import sys # for user input

conf = SparkConf().setMaster('local').setAppName('amount-spent')
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    #return int(fields[0]), float(fields[2])
    customer = int(fields[0])
    amount = float(fields[2])
    return customer, amount
    #return (customer, amount)
    # ^^^ No difference between the two

''' # DEPRECATED
def getSortMethod():
    """Solicit the user to choose how to sort the data on output."""
    print("How would you like to sort the data?")
    print("  customerID - Sort by Customer ID")
    print("  total      - Sort by Total Amount Spent")
    userInput = raw_input() # Python 2
    #userInput = input() # Python 3 (NOT TESTED)
    print("userInput = " + userInput)
    return userInput
    #return input()
#END DEPRECATION
'''

### Read data in
# Data has the form: Customer_ID,Item_ID,Amount_Spent_on_Item
lines = sc.textFile('customer-orders.csv')

### Extract needed fields
parsedLines = lines.map(parseLine)

### Manipulate data
totals = parsedLines.reduceByKey(lambda x, y: x + y)

if len(sys.argv) < 2: # User didn't provide sortMethod
    sortMethod = 'customerID'
else:
    sortMethod = sys.argv[1]

if sortMethod == 'customerID':
    results = totals.collect()
    # \/\/ Theses lines are redundant because reduceByKey()? happens to sort the
    #       data by key(customerID) anyway
    #sortedCustomers = totals.sortByKey()
    #results = sortedCustomers.collect()
elif sortMethod == 'total':
    sortedAmounts = totals.sortBy(lambda x: x[1])
    results = sortedAmounts.collect()
else:
    print("Uhh... We didn't get a valid choice.")
    exit(1)

### Output results
for result in results:
    #print result
    print str(result[0]) + ': ' + str(result[1])

