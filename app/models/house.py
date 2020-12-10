"""This module contains the House and HouseModel classes"""

import re
from bson import ObjectId
from flask import jsonify
from ..utils.various import SingletonMeta
from ..utils.errors import APIError
from ..utils.validation import validate_input
from .base import Entity, Model


def rooms_validator(rooms):
    if len(rooms) == 0:
        return False

    for room in rooms:
        if 'name' not in room or 'size' not in room:
            return False

        if type(room['name']) != str or type(room['size']) != int:
            return False

    return True


HOUSE_VALIDATION = {
    'name': {
        'required': True,
        'type': str
    },
    'address': {
        'required': True,
        'type': str
    },
    'postal_code': {
        'required': True,
        'type': str,
        'pattern': re.compile(r'^\d{5}$')
    },
    'city': {
        'required': True,
        'type': str
    },
    'rooms': {
        'required': True,
        'type': list,
        'custom_validator': rooms_validator
    }
}


class House(Entity):
    def __init__(self, id, created_by, name, address, postal_code, city, rooms) -> None:
        super().__init__()

        self.id = id
        self.created_by = created_by
        self.name = name
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.rooms = rooms

    @staticmethod
    def format_rooms(raw_rooms):
        rooms = []

        for raw in raw_rooms:
            rooms.append({
                'name': raw['name'],
                'size': raw['size']
            })

        return rooms

    @staticmethod
    def from_json(data: dict):
        """Creates a `House` instance from a JSON dictionary"""

        validate_input(HOUSE_VALIDATION, data)

        return House(
            None,
            None,
            data['name'],
            data['address'],
            data['postal_code'],
            data['city'],
            House.format_rooms(data['rooms'])
        )

    def to_json(self):
        """Creates a valid Flask response"""

        return {
            'id': self.id,
            'created_by': self.created_by,
            'name': self.name,
            'address': self.address,
            'postal_code': self.postal_code,
            'city': self.city,
            'rooms': self.rooms
        }

    def update_from_json(self, data: dict):
        """Updates the user according to a dictionary"""

        validate_input(HOUSE_VALIDATION, data, check_required=False)

        if 'name' in data:
            self.name = data['name']

        if 'address' in data:
            self.address = data['address']

        if 'postal_code' in data:
            self.postal_code = data['postal_code']

        if 'city' in data:
            self.city = data['city']

        if 'rooms' in data:
            self.rooms = House.format_rooms(data['rooms'])


class HouseModel(Model, metaclass=SingletonMeta):
    collection_name = 'houses'

    def to_entity(self, record: dict):
        return House(
            str(record['_id']),
            record['created_by'],
            record['name'],
            record['address'],
            record['postal_code'],
            record['city'],
            record['rooms']
        )

    def from_entity(self, entity):
        if entity.created_by is None:
            raise APIError('Cannot add to database a house without owner ID')

        rec = {
            'created_by': entity.created_by,
            'name': entity.name,
            'address': entity.address,
            'postal_code': entity.postal_code,
            'city': entity.city,
            'rooms': entity.rooms
        }

        if entity.id is not None:
            rec['_id'] = ObjectId(entity.id)

        return rec

    def search_by_city(self, city: str):
        records = self.collection.find({
            'city': {'$regex': city, '$options': 'i'}
        })

        if records is None:
            return []

        return list(map(self.to_entity, records))

    def get_by_owner(self, owner_id: str):
        """Returns the list of the houses of an owner"""

        records = self.collection.find({'created_by': owner_id})

        if records is None:
            return []

        return list(map(self.to_entity, records))
