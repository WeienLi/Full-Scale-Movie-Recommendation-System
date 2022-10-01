import json
import os
from pyspark.ml.recommendation import ALSModel
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType
import random

sc = SparkContext()
spark = SparkSession.builder.appName('Recommendations').getOrCreate()

def recommendMovies(userID):
    #load model
    root = os.path.join(os.path.dirname(__file__))
    model = ALSModel.load(os.path.join(root, 'ALS'))
    # read the lookup table JSON
    with open(os.path.join(root, 'lookuptable', 'lookuptable.json'), 'r') as f:
        lookup = json.load(f)
    userid_int = int(userID)
    user_subset = spark.createDataFrame([userid_int], IntegerType())
    user_subset = user_subset. \
        withColumn('userId', col('value').cast('integer')).\
        drop('value')
    try:
        rec = model.recommendForUserSubset(user_subset, 20) #model not loaded
        movie_id_rec = rec.select("recommendations.movieIndex")
        rec_list = movie_id_rec.collect()[0][0]
    except:
        rec_list = random.sample(range(1, 25533), 20)
    toreturn = []
    for movie1_id in rec_list:
        movie1_title = lookup[str(movie1_id)]
        toreturn.append(movie1_title)
    return toreturn
