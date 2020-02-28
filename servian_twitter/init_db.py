# -----------------------------------------------------------
# init_db.py
#
# Initializes the SQLite database with some starting data.
# The create_all() doesn't overwrite the existing database so
# if you run this with an existing database, there will be an
# integrity error:
#
#  > (sqlite3.IntegrityError) UNIQUE constraint failed: system_config.key
#
# -----------------------------------------------------------

from servian_twitter.models import db, SystemConfig

print ('Preparing to create database with some initial config settings...')

db.create_all()

initial_config_values = {
    'TWITTER_ACCESS_TOKEN': '1231806543030415360-8V3FC7LObpvgL7ckrewzdUjjnPuamd',
    'TWITTER_ACCESS_SECRET': 'jRvpNwBKvqiNDhkVItSj4yyCohGQNQ79VSyyCFyW5GweZ',
    'TWITTER_API_KEY': 'XJHHqegPrw0BohX8Grxp8lIOT',
    'TWITTER_API_SECRET': '6tebbwIHTN3iHbUfrlW8bOLkKGcr6cjoFPNnwpAaqxuFaeeIKF',
    'TWITTER_STREAM_KEYWORD': 'servian',
    'TWEET_QUERY_LIMIT': '100',
}

for key, value in initial_config_values.items():
    config = SystemConfig(key=key, value=value)
    db.session.add(config)

db.session.commit()

print ('Database created!')
