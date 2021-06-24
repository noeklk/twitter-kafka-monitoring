from pyspark.sql import SparkSession
import sys
spark = SparkSession.builder.getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "trump") \
    .load()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

print("df")
print(df.columns)
print(df.value)
# for i in df.columns:
#     print(i)
#     df.select(i).show(10)


query = df.writeStream.outputMode("append").format("console").start()

# Terminates the stream on abort
print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")

query.awaitTermination()