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

from servian_twitter.models import db, SystemConfig

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
    CONFIG = json.load(f)

def init_db():
    print ('Preparing to create database with some initial config settings.')

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

def copy_from_template():
    """Copy a template starting database from the travis_templates folder

    This is a workaround because the Travis CI build environment doesn't
    seem to run the init_db() function above properly.
    """
    print ('Preparing to create a new database from an existing template.')

    if not database_exists(CONFIG['SQLITE_URL']):
        import os
        import shutil

        # Source path
        source = "travis_templates/servian_twitter_template.db"

        # Destination path
        destination = "servian_twitter.db"

        # Copy the content of
        # source to destination
        dest = shutil.copyfile(source, destination)
        print ('Database created from template!')
    else:
        print ('Datbase already exists, now exiting.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'from_template':
            copy_from_template()
        else:
            init_db()
    else:
        init_db()
