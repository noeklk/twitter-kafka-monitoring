from hdfs import InsecureClient
import os
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('tweets', bootstrap_servers=['kafka:9092'])
client = InsecureClient('http://hadoop-master:9870/', user='kafka-data')

TWEET_LOOP_LIMIT = 250

def convert_to_json(b):
    df_decode = b.decode('utf8')
    df_json = json.loads(df_decode)
    return df_json

inp = []
file_count = 0

for message in consumer:
    inp.append(message.value)
    
    print(len(inp))
    
    if len(inp) >= TWEET_LOOP_LIMIT:
        filename = f'data-{file_count}.json'
        file_count += 1
        print(f"Reached the loop limit of {TWEET_LOOP_LIMIT} tweets, overwriting to hdfs to filename: {filename}")
        out = map(convert_to_json, inp)
        inp = []
        client.write(filename, data=json.dumps(list(out)), encoding='utf-8', overwrite=True)