import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_deduper

NEWS_TABLE_NAME = "news"

def test_handle_message_basic():
    db = mongodb_client.get_db()
    test_msg_1 = {
      "source": "Test 1",
      "title": "Test 1",
      "publishedAt": "2018-03-17T18:42:00Z",
      "digest":"test1",
      "text":"this is a test."
    }
    test_msg_2 = {
      "source": "Test 2",
      "title": "Test 2",
      "publishedAt": "2018-03-17T23:18:00Z",
      "digest":"test2",
      "text":"is this a test?"
    }
    test_msg_3 = {
      "source": "Test 3",
      "title": "Test 3",
      "publishedAt": "2018-03-17T23:18:00Z",
      "digest":"test3",
      "text":"this is a new test!"
    }
    none_message = None
    
    db[NEWS_TABLE_NAME].insert(test_msg_1)
    count = db[NEWS_TABLE_NAME].count()

    news_deduper.handle_message(none_message)
    count_1 = db[NEWS_TABLE_NAME].count()
    assert count_1 == count
    print("null check passed")

    news_deduper.handle_message(test_msg_1)
    count_2 = db[NEWS_TABLE_NAME].count()
    assert count_2 == count
    print("duplicate check passed")

    news_deduper.handle_message(test_msg_2)
    count_3 = db[NEWS_TABLE_NAME].count()
    assert count_3 == count

    news_deduper.handle_message(test_msg_3)
    count_4 = db[NEWS_TABLE_NAME].count()
    assert count_4 == count + 1
    print("handle_message test passed")

    db[NEWS_TABLE_NAME].remove({"title": "Test 1"})
    db[NEWS_TABLE_NAME].remove({"title": "Test 2"})
    db[NEWS_TABLE_NAME].remove({"title": "Test 3"})

if __name__ == "__main__":
    test_handle_message_basic()


   
