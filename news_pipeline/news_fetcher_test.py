import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient
import news_fetcher

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://wzvsnapn:EbX7UVQN4UxCE56odlSJh_8wIA87mIaM@skunk.rmq.cloudamqp.com/wzvsnapn"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def test_handle_message_basic():
    test_msg = {
      "source": "The Wall Street Journal",
      "title": "Berkshire Hathaway Benefits From US Tax Plan",
      "description": "Berkshire Hathaway posted a $29 billion gain in 2017 related to changes in U.S. tax law, a one-time boost that inflated annual profits for the Omaha conglomerate.",
      "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
      "urlToImage": "https://si.wsj.net/public/resources/images/BN-XP717_3812B_TOP_20180224064100.jpg",
      "publishedAt": "2018-02-24T18:42:00Z",
      "digest":"3RjuEomJo26O1syZbU7OHA==\n",
      "reason": "Recommend"
    }

    none_msg = None

    #test handle_message ignore none message
    dedupe_news_queue_client.send_message(test_msg)
    news_fetcher.handle_message(none_msg)
    msg_1 = dedupe_news_queue_client.get_message()
    dedupe_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    assert msg_1 == test_msg
    print("handle_message works fine with null input!")

    #test handle_message is able to add text
    news_fetcher.handle_message(test_msg)
    dedupe_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    msg_2 = dedupe_news_queue_client.get_message()
    assert len(msg_2['text']) > 0
    print("handle_message test passed")

if __name__ == "__main__":
    test_handle_message_basic()


