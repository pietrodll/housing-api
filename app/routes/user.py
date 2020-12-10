"""This module contains the blueprint for the /user route"""

from flask import Blueprint, request
from flask_jwt import jwt_required, current_identity
from ..utils.errors import ValidationError
from ..models.user import UserModel


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/me', methods=('GET',))
@jwt_required()
def get_me():
    """Gets the current user"""

    return current_identity.to_json()


@bp.route('/me', methods=('PUT',))
@jwt_required()
def edit_me():
    """Edits the current user"""

    if request.json is None:
        raise ValidationError('Body cannot be empty')

    current_identity.update_from_json(request.json)

    updated = UserModel().replace(current_identity)

    return updated.to_json()
