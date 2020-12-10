from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from .utils.errors import ValidationError
from .models.user import User, UserModel

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST',))
def register():
    password = request.json['password']

    if not password or type('password') != str:
        return ValidationError('Invalid password')

    user = User.from_json(request.json)
    user.password_hash = generate_password_hash(password)

    UserModel().insert(user)

    return 'OK'


# /login is already handled by Flask-JWT

def authenticate(email, password):
    """Login function"""

    user = UserModel().get_by_email(email)

    if check_password_hash(user.password_hash, password):
        return user

    return None


def identity(payload):
    user_id = payload['identity']
    return UserModel().get_by_id(user_id)
