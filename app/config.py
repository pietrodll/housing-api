"""Configuration file for the Flask app"""

import os
from datetime import timedelta


SECRET_KEY = os.getenv('SECRET_KEY')


def get_database_url():
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PWD')
    db_host = os.getenv('DB_HOST')

    return f'mongodb://{db_user}:{db_password}@{db_host}'


DATABASE_URL = get_database_url()
DATABASE_NAME = os.getenv('DB_NAME')


# ─── FLASK JWT CONFIGURATION ────────────────────────────────────────────────────

JWT_AUTH_USERNAME_KEY = 'email'
JWT_AUTH_PASSWORD_KEY = 'password'
JWT_AUTH_URL_RULE = '/auth/login'
JWT_AUTH_HEADER_PREFIX = 'Bearer'
JWT_EXPIRATION_DELTA = timedelta(hours=1)
