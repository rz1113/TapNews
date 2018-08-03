""""mongodb client"""
from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017' # default port
DB_NAME = 'tap-news' #database name which may connect many collection

# singelton client
client = MongoClient("%s:%s" %(MONGO_DB_HOST, MONGO_DB_PORT))
# if there is no argument,use the defualt DB_NAME
# Othewise, use the passed in argument
def get_db(db=DB_NAME):
    """get database instance"""
    db = client[db]
    return db
