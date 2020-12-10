"""This module contains various Exception subclasses"""

from flask import jsonify


class APIError(Exception):
    """General class for API errors"""

    status_code = 500
    error_name = 'API_ERROR'

    def __init__(self, message='') -> None:
        super().__init__(self)
        self.message = message

    def to_json(self):
        response = jsonify(error_name=self.error_name, message=self.message)
        response.status_code = self.status_code

        return response


class ValidationError(APIError):
    """This exception is raised when a user input is incorrect and results to a 400 HTTP status"""

    status_code = 400
    error_name = 'VALIDATION_ERROR'


class NotFoundError(APIError):
    """This exception is raised when a query leads to no results"""

    status_code = 404
    error_name = 'NOT_FOUND_ERROR'
