from pymongo import MongoClient

def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://mechy:<password>@irsrp-cluster-0.onx2rrm.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    db = client.test
    return db