"""Backend Service"""
import operations
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

#use this funtion for testing
def add(num1, num2):
    """ Add two numbers. """
    print("add is called with %d and %d" % (num1, num2))
    return num1 + num2

def get_one_news():
    """ Get one news. """
    print("getOneNews is called")
    return operations.get_one_news()

def get_news_summaries_for_user(user_id, page_num):
    """Get news summuaries for a user with user_id and page number"""
    print("get_news_summaries_for_user is called with %s and %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)

def log_news_click_for_user(user_id, news_id):
    print("log_news_click_for_user is called with %s and %s" % (user_id, news_id))
    operations.logNewsClickForUser(user_id, news_id)

#Threading RPC Server    
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
#expose the addAPI. map add function to'add' API
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'getOneNews')
RPC_SERVER.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
RPC_SERVER.register_function(log_news_click_for_user, 'logNewsClickForUser')
print("Starting RPC server on %s: %d" %(SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()

 