# %%
import pymongo
from environs import Env


def get_db_connection():
    env = Env()
    env.read_env()
    db_url = env("mongodb_uri")
    dbClient = pymongo.MongoClient(db_url)

    return dbClient
