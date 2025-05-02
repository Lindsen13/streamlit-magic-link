import os

from pymongo.mongo_client import MongoClient

DATABASE_NAME = os.environ.get("DATABASE_NAME", "streamlit-magic-link")
COLLECTION_NAME_USERS = os.environ.get("COLLECTION_NAME_USERS", "users")
COLLECTION_NAME_MAGIC_LINKS = os.environ.get("COLLECTION_NAME_MAGIC_LINKS", "magic-links")


def get_user_collection(client: MongoClient):
    """
    Get the user collection from the MongoDB client.
    """
    database = client.get_database(DATABASE_NAME)
    users = database.get_collection(COLLECTION_NAME_USERS)
    return users


def get_magic_link_collection(client: MongoClient):
    """
    Get the magic link collection from the MongoDB client.
    """
    database = client.get_database(DATABASE_NAME)
    magic_links = database.get_collection(COLLECTION_NAME_MAGIC_LINKS)
    return magic_links
