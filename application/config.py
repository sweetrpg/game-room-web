__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
config.py
- settings for the flask application object
"""


import os
import redis
import random
import hashlib


class BaseConfig(object):
    DEBUG = bool(os.environ.get('DEBUG') or True)
    ASSETS_DEBUG = True
    POSTGRES_HOST = os.environ["PGHOST"]
    POSTGRES_PORT = os.environ["PGPORT"] or "5432"
    POSTGRES_USER = os.environ["PGUSER"]
    POSTGRES_PW = os.environ["PGPASSWORD"]
    POSTGRES_DB = os.environ["PGDATABASE"]
    DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///survey.db'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or hashlib.sha256(f"{random.random()}").hexdigest()
    CSRF_TOKEN = os.environ.get('CSRF_TOKEN') or hashlib.sha256(f"{random.random()}").hexdigest()
    CACHE_REDIS_HOST = os.environ['REDIS_HOST']
    CACHE_REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    # CACHE_REDIS_DB = int(os.environ.get('REDIS_DB') or 7)
    VUE_USE_MINIFIED = True
    VUE_CDN_FORCE_SSL = True
    VUE_LOCAL_SUBDOMAIN = None
    VUE_CONFIGURATION = {}
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(f"redis://{os.environ['REDIS_HOST']}:{int(os.environ.get('REDIS_PORT') or 6379)}")
