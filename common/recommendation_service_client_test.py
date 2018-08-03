import recommendation_service_client as client

def test_basic():
    userId = "test_user"
    perfernce = client.getPreferenceForUser(userId)
    assert perfernce is not None
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
