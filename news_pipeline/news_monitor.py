import datetime 
import hashlib #md5 hash 
import redis 
import os #used for import common 
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import news_api_client 
from cloudAMQP_client import CloudAMQPClient

#every 10 second for every loop ,may consider to set a longer time 
SLEEP_TIME_IN_SECONDS = 10 
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3  #news expires in 3 days

REDIS_HOST = 'localhost' 
REDIS_PORT = 6379

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://fnicgqhk:jjBItDmsUVKBZ0Yq1tE0WVbe9ViUjvMw@skunk.rmq.cloudamqp.com/fnicgqhk"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

#connect redis client and cloudAMQP client
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def run():
    while True:
        news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)
        num_of_new_news = 0

        for news in news_list:
            # calculate MD5 and convert to string use hexigest
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
            if redis_client.get(news_digest) is None:
                num_of_new_news += 1
                # every news has unique digest
                news['digest'] = news_digest

                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                
                # use as hash set, value does not matter
                redis_client.set(news_digest, "True")
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

                cloudAMQP_client.send_message(news)

        print("Fetched %d news." % num_of_new_news)

        # use cloudAMQP_client.sleep keep queue heartbeat
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__" :
    run()


