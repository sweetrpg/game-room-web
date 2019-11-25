__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""


from flask_caching import Cache


cache = Cache(config={'CACHE_TYPE': 'redis'})
