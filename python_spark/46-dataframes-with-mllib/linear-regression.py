# linear-regression.py
# August 9, 2020
#
#

from __future__ import print_function

# DataFrame APIs in ml library, not MLLib
from pyspark.ml.regression import LinearRegression

from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors

if __name__ == "__main__":
    spark = SparkSession.builder.appName("LinearRegression").getOrCreate()

    # Load data and convert it to the format MLLib expects
    #   (label (feature, feature, feature, ...))
    #   (any type?, dense? Vector)
    inputLines = spark.sparkContext.textFile("regression.txt")
    data = inputLines.map(lambda x: x.split(",")).map(lambda x: (float(x[0]), Vectors.dense(float(x[1]))))

    # Convert RDD to DataFrame
    # If you are importing data from a structured source, such as a database or
    #       JSON, you can read it directly into a DataFrame
    colNames = ["label", "features"]
    df = data.toDF(colNames)

    # Split data into training and testing data
    trainTest = df.randomSplit([0.5, 0.5])
    trainingDF = trainTest[0]
    testDF = trainTest[1]

    # Create linear regression model
    lir = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

    # Train the model
    model = lir.fit(trainingDF)

    # Evaluate model on testing data
    # Generate predictions using out linear regression model for all features in
    # our test dataframe
    fullPredictions = model.transform(testDF).cache()

    # Extract the predictions and the "known" correct labels
    predictions = fullPredictions.select("prediction").rdd.map(lambda x: x[0])
    labels = fullPredictions.select("label").rdd.map(lambda x: x[0])

    predictionAndLabel = predictions.zip(labels).collect()

    # Print results
    for example in predictionAndLabel:
        print(example)

