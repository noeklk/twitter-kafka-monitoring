from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import os
import json
from kafka import KafkaProducer

ACCESS_TOKEN="1052919765126316033-eATAf2skyDxIomK4GxYaZ7zj5Th6BX"
ACCESS_TOKEN_SECRET="fMFNeiSTpMu4kJuZx0vXYgKeizRGv8CZZQaZ2LbY576lH"
CONSUMER_KEY="0wjVKNcrlxQIlf0UKVNwpwShq"
CONSUMER_SECRET="mUoz9LP810L2bkJzfpM1e8TgK2wLmip3kc7nORjvAbwwmtKxid"

SEARCH_KEYWORD = str(input("Please enter a keyword to filter\n"))

producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

class StdOutListener(StreamListener):
    def __init__(self):
        self.count=0

    def on_data(self, data):
        producer.send("tweets", data.encode('utf-8'))
        self.count+=1
        print(self.count)
        return True
    def on_error(self, status):
        print (status)

myStreamListener = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
myStream = tweepy.Stream(auth = auth, listener=myStreamListener)
myStream.filter(track=[SEARCH_KEYWORD])

print(f"Starting tweet streams")