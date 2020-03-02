import os
import tempfile
import pytest
import json
import datetime

from servian_twitter import app, socketio
from servian_twitter.models import db, Tweet, SystemConfig
from servian_twitter.init_db import init_db

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
    CONFIG = json.load(f)

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG['SQLITE_TEST_DB_NAME'])
db_uri = 'sqlite:///{}'.format(db_path)

@pytest.fixture
def client():
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri
    }

    # Establish an application context before running the tests.
    for key, value in settings_override.items():
        app.config[key] = value

    with app.test_client() as client:
        yield client


@pytest.fixture
def _db():
    with app.app_context():
        init_db(CONFIG['SQLITE_TEST_DB_NAME'])
        yield db

    db.drop_all()
    os.unlink(db_path)

def test_socketio_connection(client):
    """Tests that our socketio server works"""

    # connect to Socket.IO
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # make sure the server accepted the connection
    r = socketio_test_client.is_connected()
    assert r == True

    test_data = dict(
        tweet_id = '234234234',
        avatar_color_index = '1',
        stream_keyword = 'python',
        created_at = datetime.datetime.now(),
        hashtags = 'these are some hashtags',
        text = 'tweet text',
        user = 'user name',
        user_loc = 'user location',
    )

    # Send some mock data from socketio server
    # In the real scenario, 'here_are_tweets' messages are sent
    # via twitter_streamer's ServianTwitterStreamer class
    socketio.emit('here_are_tweets', test_data)

    r = socketio_test_client.get_received()

    # Check that the message content is consistent
    assert len(r) == 1
    assert r[0]['args'][0]['tweet_id'] == test_data['tweet_id']
