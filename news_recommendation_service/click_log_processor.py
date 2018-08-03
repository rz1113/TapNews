# -*- coding: utf-8 -*-

'''
Time decay model:
If selected:
p = (1-α)p + α
If not:
p = (1-α)p
Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.

Update model every day
'''
import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

NUM_OF_CLASS = 8
INITIAL_P = 1.0 / NUM_OF_CLASS
#when alpha is large,the recent click event have more effect on the model 
#for example, assume we set alpha as a very large number.
#the most of thenewsaclientclicksaresportnewsinthepast10days,and this client click on a u.s news now, the system will change the user's preference to u.s news.
ALPHA = 0.1

LOG_CLICKS_TASK_QUEUE_URL = "amqp://dbretdrp:KbusFR8WuYn4qz-uJ8VTwUEcU8eQzN9q@wombat.rmq.cloudamqp.com/dbretdrp"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-clicks-task-queue"
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECOND = 3

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"  

def handleMessage(msg):
    if msg is None or not isinstance(msg, dict):
        return
    
    if ('userId' not in msg or 'newsId' not in msg or 'timestamp' not in msg):
        return
    
    userId = msg['userId']
    newsId = msg['newsId']
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    if model is None:
        print('Creating new model for user: %s' %userId)
        news_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        news_model['preference'] = preference
        model = news_model
    
    #Update model using time decay model
    print("Update preference model for user: %s" %userId)
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None or news['class'] is None or news['class'] not in news_classes.classes):
        print("Skipping processing")
        return
    
    #update the click one
    click_class = news['class']
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    #Update the non-click classes
    for i, prob in model['preference'].items():
        if not i == click_class:
            old_p = model['preference'][i]
            model['preference'][i] = float((1 - ALPHA) * old_p)
    
    #upsert = true: if not exist, insert new one
    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)


def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.get_message()
            if msg is not None:
                try:
                    handleMessage(msg)
                except Exception as e:
                    print(e)
                    pass
            
            #sleep
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECOND)

if __name__ == "__main__":
    run()
                


