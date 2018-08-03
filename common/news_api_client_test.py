import news_api_client as client 

def test_basic():
# test pass with no argument
    news = client.getNewsFromSources()
    print(news)
    assert len(news) > 0
    # test pass with argument
    news = client.getNewsFromSources(sources=['cnn'], sortBy='top')
    assert len(news) > 0
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()