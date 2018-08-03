"""Backend Service Operations"""
import json
import os
import sys
import redis
import pickle
from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
import recommendation_service_client

REDIS_HOST = "localhost"
REDIS_PORT = 6379

NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 200
NEWS_TABLE_NAME = "news"
USER_NEWS_TIME_OUT_IN_SECONDS = 60

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

LOG_CLICKS_TASK_QUEUE_URL = "amqp://dbretdrp:KbusFR8WuYn4qz-uJ8VTwUEcU8eQzN9q@wombat.rmq.cloudamqp.com/dbretdrp"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-clicks-task-queue"
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def get_one_news():
    """get one news"""
    print("getOneNews is called")
    res = mongodb_client.get_db()['news'].find_one()
    return json.loads(dumps(res))

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    # news range to be fetched for the page number 
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # the final list of news to be returned
    sliced_news = []

    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        # user id already cached in redis, get next paginating data and fetch news
        news_digest = pickle.loads(redis_client.get(user_id))
        sliced_news_digest = news_digest[begin_index : end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digest}}))

    else:
        # no cached data
        # retrieve news and store their digests list in redis with user id as key
        # retrieve news and sort by published time in reverse order(latest first)

        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digest = [x['digest'] for x in total_news]

        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index : end_index]

    # get preference
    preference = recommendation_service_client.getPreferenceForUser(user_id)
    topPerference = None

    if preference is not None and len(preference) > 0:
        topPerference = preference[0]
        
    for news in sliced_news:
        # Remove text field to save bandwidth
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            #Add time tag to be displayed on page
            news['time'] = 'today'
        if news['class'] == preference:
            news['reason'] = 'Recommend'
            
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}

    # Send log task to click log processor
    cloudAMQP_client.send_message(message)


