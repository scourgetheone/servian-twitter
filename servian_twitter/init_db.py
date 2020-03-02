# -----------------------------------------------------------
# init_db.py
#
# Initializes the SQLite database with some starting data.
#
# -----------------------------------------------------------
from sqlalchemy_utils import database_exists
import os
import json
import sys


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
    CONFIG = json.load(f)

def init_db():
    print ('Preparing to create database with some initial config settings.')

    from servian_twitter.models import db, SystemConfig

    if not database_exists(CONFIG['SQLITE_URL']):
        db.create_all()

        initial_config_values = {
            'TWITTER_ACCESS_TOKEN': '1231806543030415360-8V3FC7LObpvgL7ckrewzdUjjnPuamd',
            'TWITTER_ACCESS_SECRET': 'jRvpNwBKvqiNDhkVItSj4yyCohGQNQ79VSyyCFyW5GweZ',
            'TWITTER_API_KEY': 'XJHHqegPrw0BohX8Grxp8lIOT',
            'TWITTER_API_SECRET': '6tebbwIHTN3iHbUfrlW8bOLkKGcr6cjoFPNnwpAaqxuFaeeIKF',
            'TWITTER_STREAM_KEYWORD': 'python',
            'TWEET_QUERY_LIMIT': '100',
        }

        for key, value in initial_config_values.items():
            try:
                config = SystemConfig(key=key, value=value)
                db.session.add(config)
                db.session.commit()
            except Exception as e:
                print ('Error while trying to add initial values')
                print (e)

        print ('Database created!')
    else:
        print ('Datbase already exists, now exiting.')


if __name__ == '__main__':
    init_db()
