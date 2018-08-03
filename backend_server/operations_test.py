"""Backend Service Operations Test"""
import operations

def test_get_one_news_basic():
    """Test Get one news method"""
    news = operations.get_one_news()
    print(news)
    assert news is not None
    print('test_get_one_news_basic passed!')

def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser('test', 1)
    assert len(news) > 0
    print('test_getNewsSummariesForUser_basic passed!')

def test_getNewsSummariesForUser_pagination():
    news_page_1 = operations.getNewsSummariesForUser('test', 1)
    news_page_2 = operations.getNewsSummariesForUser('test', 2)
    #  Assert that there is no dupe news in two pages
    digests_set_1 = set([news['digest'] for news in news_page_1])
    digests_set_2 = set([news['digest'] for news in news_page_2])

    assert len(digests_set_1.intersection(digests_set_2)) == 0
    print('test_getNewsSummariesForUser_pagination passed!')
     

if __name__ == "__main__":
    test_get_one_news_basic()
    test_getNewsSummariesForUser_basic()
    test_getNewsSummariesForUser_pagination()
