import operator
import os
import sys

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getPreferenceForUser(userId):
    """ Get user's pereference in an ordered class list """
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    # if this is a new user, there is no preference
    if model is None:
        return []
    
    # sort by the perference value in descending order
    sorted_tuples = sorted(list(model['preference'].items()),
        key = operator.itemgetter(1), reverse=True)
    # get all the key
    sorted_list = [x[0] for x in sorted_tuples]
    # get all the value
    sorted_value_list = [x[1] for x in sorted_tuples]

    # if all the preference are the same, there is no perference
    # since the array is sorted, we just need to compare the first and the last
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []
    
    return sorted_list

# Threading HTTP Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')

print("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
