"""
config.py
- settings for the flask application object
"""

import os


class BaseConfig(object):
    DEBUG = True
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"] or "5432"
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PW = os.environ["POSTGRES_PW"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///survey.db'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = 'mysecretkey'
