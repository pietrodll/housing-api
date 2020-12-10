"""This module contains the blueprint for the /house route"""

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required, current_identity
from ..utils.errors import ForbiddenError, NotFoundError
from ..models.house import HouseModel, House


bp = Blueprint('house', __name__, url_prefix='/house')


@bp.route('', methods=('GET',))
@jwt_required()
def get_all_houses():
    """Returns all the houses"""

    houses = HouseModel().list()
    return jsonify([house.to_json() for house in houses])


@bp.route('', methods=('POST',))
@jwt_required()
def add_house():
    """Adds a new house to the database"""

    house = House.from_json(request.json)
    house.created_by = current_identity.id

    HouseModel().insert(house)

    return 'OK'


@bp.route('/search', methods=('GET',))
@jwt_required()
def search_houses():
    if 'city' not in request.args:
        houses = HouseModel().list()
        return jsonify([house.to_json() for house in houses])

    city = request.args['city']

    houses = HouseModel().search_by_city(city)

    return jsonify([house.to_json() for house in houses])


@bp.route('/<house_id>', methods=('PUT',))
@jwt_required()
def edit_house(house_id):
    house = HouseModel().get_by_id(house_id)

    if house is None:
        raise NotFoundError(
            f'Could not find house with the following ID: {house_id}')

    if house.created_by != current_identity.id:
        raise ForbiddenError('Cannot edit someone else\'s house!')

    house.update_from_json(request.json)
    updated = HouseModel().replace(house)

    return updated.to_json()
