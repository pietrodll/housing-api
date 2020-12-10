import pymongo
from flask import current_app, g
from .utils.various import SingletonMeta


class DBClient(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(current_app.config['DATABASE_URL'])
        self.db = self.client[current_app.config['DATABASE_NAME']]


def close_db(e=None):
    client = DBClient()

    del client
