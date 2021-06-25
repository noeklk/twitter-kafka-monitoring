from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as f


spark = SparkSession.builder.getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "spark_tweets") \
  .option("startingOffsets", "latest") \
  .load().selectExpr("CAST(value AS STRING)")

tweetSchema = StructType([ \
  StructField("timestamp", TimestampType()), StructField("hashtags", StringType())])


def parse_data_from_kafka_message(sdf, schema):
  from pyspark.sql.functions import split
  assert sdf.isStreaming == True, "DATA Frame Doesing't stream"

  col = split(sdf['value'], ",") #split attributes to nested array in one Column
  #now expand col to multiple top-level columns
  for idx, field in enumerate(schema): 
    sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
  return sdf.select([field.name for field in schema])

df = parse_data_from_kafka_message(df, tweetSchema)

query = df.groupBy("hashtags").count().sort(f.desc("count"))

query.writeStream.outputMode("complete").format("console").option("truncate", False).start().awaitTermination()