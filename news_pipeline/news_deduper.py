import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
import news_topic_modeling_service_client

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://wzvsnapn:EbX7UVQN4UxCE56odlSJh_8wIA87mIaM@skunk.rmq.cloudamqp.com/wzvsnapn"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 1

#change the table that store the news
NEWS_TABLE_NAME = "new_news"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    
    task = msg
    text = task['text']
    if text is None:
        return
    
    #Get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()

    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}
    ))

    #print("=============== in same_day_list" + str(same_day_news_list))
    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        #calculate similarity matrix

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        print(pairwise_sim)

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                #Duplicated news
                print("Duplicated news. Ignore.")
                return
    
    task['publishedAt'] = parser.parse(task['publishedAt'])

    #Classify topic
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['task'] = topic
        print(str(topic))

    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.get_message()
            if msg is not None:
                try: 
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass

            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()