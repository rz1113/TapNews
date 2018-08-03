"""CloudAMQP client Test"""
from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://sckbgqap:-5emLN1Gm9D_jjio_5XLtHPoJmxDpTlk@wombat.rmq.cloudamqp.com/sckbgqap"
QUEUE_NAME = "test"

def test_basic():
    """"Test method"""
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sent_message = {'test':'test'}
    client.send_message(sent_message)
    received_message = client.get_message()
    assert sent_message == received_message
    print('test_basic passed.')

if __name__ == "__main__":
    test_basic()
    