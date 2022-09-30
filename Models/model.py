# Import the model here
import numpy as np 
import pandas as pd
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer
from pyspark.sql.types import StructType,StructField, StringType, IntegerType

sc = SparkContext()
spark = SparkSession.builder.appName('Recommendations').getOrCreate()

def recommendMovies(userID):
    #load model
    model = ALSModel.load("ALS")
    # load lookup table csv
    lookup = spark.read.csv("lookuptable",sep = ',', header = True)
    userid_int = int(userID)
    user_subset = spark.createDataFrame([userid_int], IntegerType())
    user_subset = user_subset. \
        withColumn('userId', col('value').cast('integer')).\
        drop('value')
    rec = model.recommendForUserSubset(user_subset, 20) #model not loaded
    movie_id_rec = rec.select("recommendations.movieIndex")
    rec_list = movie_id_rec.collect()[0][0]
    toreturn = []
    for movie1_id in rec_list:
        final = lookup.filter(lookup.movieIndex == movie1_id)
        Done = final.select("movieID")
        toreturn.append(Done.collect()[0][0])
    return toreturn
