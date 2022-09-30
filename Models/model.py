import os
from pyspark.ml.recommendation import ALSModel
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType

sc = SparkContext()
spark = SparkSession.builder.appName('Recommendations').getOrCreate()

def recommendMovies(userID):
    #load model
    root = os.path.join(os.path.dirname(__file__))
    model = ALSModel.load(os.path.join(root, 'ALS'))
    # load lookup table csv
    lookup = spark.read.csv(os.path.join(root, 'lookuptable'),sep = ',', header = True)
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
