import json
import os

from pyspark import SparkContext
from pyspark.sql import SparkSession

sc = SparkContext()
spark = SparkSession.builder.appName("Recommendations").getOrCreate()

root = os.path.join(os.path.dirname(__file__))
lookup = spark.read.csv(
    os.path.join(root, "part-00000-c2006f7e-6158-4e06-99c6-daf26d9aefb9-c000.csv"),
    sep=",",
    header=True,
)
output = {}

for row in lookup.collect():
    output[int(row[1])] = row[0]

# save json
with open(os.path.join(root, "lookuptable.json"), "w") as f:
    json.dump(output, f)
