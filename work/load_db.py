#!/usr/bin/env python3
# packages
from functools import reduce
import json
from pymongo import MongoClient
from pyspark.sql import SparkSession
# custom
from modules.udf import ms_to_display_string
from modules.utils import import_spark_df, import_json, clear_avg

# Init Spark
spark = SparkSession.builder.getOrCreate()
# Init MongoClient
client = MongoClient(
    'mongo',
    port=27017,
    username='root',
    password='root',
    authMechanism='SCRAM-SHA-256'
)
db = client.spotify
# Read CSV
# df = spark.read.format('csv') \
#     .options(header=True, inferSchema=True) \
#     .load('data/Spotify/genres_v2.csv')

# Read cs from HDFS
df = spark.read.format('csv').options(header=True, inferSchema=True).load(
    '/home/jovyan/work/data/Spotify/genres_v2.csv')
    
# Clean CSV
df = df.drop('mode') \
    .drop('key') \
    .drop('analysis_url') \
    .drop('Unnamed: 0') \
    .drop('title') \
    .drop('uri')
# Add readable duration
df = df.withColumn(
    'duration_display',
    ms_to_display_string(df.duration_ms)
)
# Import songs in db
print('Import songs in db')
import_spark_df(db, df, 'songs')


# Prepare correlations
def calc_cols_corr(corr_table, items):
    base_col, cols = items
    return corr_table + [
        {
            'base_col': base_col,
            'compared_col': col,
            'value': df.corr(base_col, col)
        } for col in cols
    ]


correlations = {
    'danceability': [
        'energy',
        'loudness',
        'valence',
        'tempo',
        'liveness',
        'instrumentalness',
        'speechiness',
        'acousticness'
    ],
    'valence': [
        'energy',
        'loudness',
        'tempo',
        'liveness',
        'instrumentalness',
        'speechiness',
        'acousticness',
    ]
}

corr_table = reduce(
    calc_cols_corr,
    list(correlations.items()),
    []
)
# Import correlations in db
print('Import correlations in db')
import_json(db, corr_table, 'correlations')

# Prepare genres
genres = df.groupBy(df.genre).agg({
    'loudness': 'avg',
    'energy': 'avg',
    'tempo': 'avg',
    'liveness': 'avg',
    'instrumentalness': 'avg',
    'speechiness': 'avg',
    'acousticness': 'avg',
    'danceability': 'avg',
    'valence': 'avg',
    'duration_ms': 'avg',
})

next_schema = [clear_avg(col_name) for col_name in genres.schema.names]
genres = genres.toDF(*next_schema)
genres = genres.withColumn(
    'duration_display',
    ms_to_display_string(genres.duration_ms)
)
# Import genres in db
print('Import genres in db')
import_spark_df(db, genres, 'genres')

# prepare count by genres
genres = [line.genre for line in df.select('genre').distinct().collect()]
counts = [
    {
        'genre': genre,
        'value': df.filter(df.genre == genre).count()
    } for genre in genres
]
counts.insert(0, {'genre': 'all', 'value': df.count()})
# Import counts by genre in db
print('Import counts in db')
import_json(db, counts, 'counts')
