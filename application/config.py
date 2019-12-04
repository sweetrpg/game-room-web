__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
config.py
- settings for the flask application object
"""


import os
import redis


class BaseConfig(object):
    DEBUG = bool(os.environ.get('DEBUG') or True)
    ASSETS_DEBUG = True
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"] or "5432"
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PW = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///survey.db'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'seekrat'
    CACHE_REDIS_HOST = os.environ['REDIS_HOST']
    CACHE_REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    # CACHE_REDIS_DB = int(os.environ.get('REDIS_DB') or 7)
    VUE_USE_MINIFIED = True
    VUE_CDN_FORCE_SSL = True
    VUE_LOCAL_SUBDOMAIN = None
    VUE_CONFIGURATION = {}
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(f"redis://{os.environ['REDIS_HOST']}:{int(os.environ.get('REDIS_PORT') or 6379)}")
