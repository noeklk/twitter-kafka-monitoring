#!/usr/bin/env python3
from pyspark.sql import SparkSession
import sys
spark = SparkSession.builder.getOrCreate()

df = spark.read.format('csv').options(header=True, inferSchema=True).load('/home/jovyan/work/data/Spotify/genres_v2.csv')
df.write.csv("hdfs://hadoop-master:9000/spotify_final_data")
print("data inserted successfully")
