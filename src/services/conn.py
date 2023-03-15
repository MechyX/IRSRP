from logger import get_logger
from pymongo import MongoClient

logger = get_logger(__name__)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://mechy:subhamechyir@irsrp-cluster-0.onx2rrm.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    create_collection(client.irsrp)
    db = client.irsrp
    try:
        db.get_collection("papers")
    except Exception as _e:
        logger.info("Papers collection does not exist, creating one...")
        create_collection()

    return client.irsrp.papers


def create_collection(db):
    db.create_collection("papers")
