"""This module contains the User and the UserModel classes"""

import re
from datetime import datetime
from bson import ObjectId
from flask import jsonify
from ..utils.various import SingletonMeta
from ..utils.validation import validate_input
from .base import Entity, Model


USER_VALIDATION = {
    'email': {
        'required': True,
        'type': str
    },
    'first_name': {
        'required': True,
        'type': str
    },
    'last_name': {
        'required': True,
        'type': str
    },
    'birth_date': {
        'required': True,
        'type': str,
        'pattern': re.compile(r'^\d{4}-\d{2}-\d{2}$')
    }
}


class User(Entity):
    def __init__(self, id: str, email: str, password_hash: str, first_name: str, last_name: str, birth_date: datetime) -> None:
        super().__init__()

        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    @staticmethod
    def from_json(data: dict):
        """Creates a `User` instance from a JSON dictionary"""

        validate_input(USER_VALIDATION, data)

        return User(
            None,
            data['email'],
            None,
            data['first_name'],
            data['last_name'],
            datetime.fromisoformat(data['birth_date'])
        )

    def to_json(self):
        """Creates a valid Flask response"""

        return jsonify({
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat()
        })

    def update_from_json(self, data: dict):
        """Updates the user according to a dictionary"""

        validate_input(USER_VALIDATION, data, check_required=False)

        if 'last_name' in data:
            self.last_name = data['last_name']

        if 'first_name' in data:
            self.first_name = data['first_name']

        if 'birth_date' in data:
            self.birth_date = datetime.fromisoformat(data['birth_date'])


class UserModel(Model, metaclass=SingletonMeta):
    collection_name = 'users'

    def to_entity(self, record: dict):
        return User(
            str(record['_id']),
            record['email'],
            record['password_hash'],
            record['first_name'],
            record['last_name'],
            datetime.fromisoformat(record['birth_date']),
        )

    def from_entity(self, entity):
        rec = {
            'email': entity.email,
            'password_hash': entity.password_hash,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'birth_date': entity.birth_date.isoformat(),
        }

        if entity.id is not None:
            rec['_id'] = ObjectId(entity.id)

        return rec

    def get_by_email(self, email: str):
        result = self.collection.find_one({'email': email})
        return self.to_entity(result)
