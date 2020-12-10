"""This module contains the abstract classes Entity and Model to be used as base for all the entities and models"""

from abc import ABCMeta, abstractmethod, abstractstaticmethod
from bson import ObjectId
from pymongo import ReturnDocument
from ..utils.various import SingletonMeta
from ..db import DBClient


class Entity(metaclass=ABCMeta):
    """Class representing an entity"""

    @abstractstaticmethod
    def from_json(data: dict):
        """Creates an instance of the class from a JSON dictionary. Includes fields validation"""

    @abstractmethod
    def to_json(self):
        """Returns a valid Flask response"""

    @abstractmethod
    def update_from_json(self, data: dict):
        """Updates the entity from a dictionary"""


class Model(metaclass=SingletonMeta):
    """Class representing a model in the database"""

    collection_name = None

    def __init__(self) -> None:
        self.db = DBClient()
        self.collection = self.db.db[self.collection_name]

    @abstractmethod
    def to_entity(self, record: dict):
        """Converts a database record to an `Entity` object"""

    @abstractmethod
    def from_entity(self, entity):
        """Converts an entity to a dictionary to be inserted in the database"""

    def get_by_id(self, id: str):
        """Gets an entity by ID"""

        record = self.collection.find_one(ObjectId(id))
        return self.to_entity(record)

    def insert(self, entity):
        rec = self.from_entity(entity)

        result = self.collection.insert_one(rec)
        return result

    def replace(self, entity):
        updated = self.collection.find_one_and_replace(
            {'_id': ObjectId(entity.id)},
            self.from_entity(entity),
            return_document=ReturnDocument.AFTER
        )

        return self.to_entity(updated)
