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

@pytest.fixture
def client():
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': CONFIG['SQLITE_TEST_URL']
    }

    # Establish an application context before running the tests.
    for key, value in settings_override.items():
        app.config[key] = value

    with app.test_client() as client:
        yield client


@pytest.fixture
def _db():
    with app.app_context():
        init_db(CONFIG['SQLITE_TEST_URL'])
        yield db
        db.drop_all()
        db.session.commit()

    db.drop_all()
    os.unlink(CONFIG['SQLITE_TEST_PATH'])


def test_create_tweet(_db, client):
    """Create some tweets"""
    test_data = dict(
        tweet_id = '123123123',
        avatar_color_index = '1',
        stream_keyword = 'python',
        created_at = datetime.datetime.now(),
        hashtags = 'these are some hashtags',
        text = 'tweet text',
        user = 'user name',
        user_loc = 'user location',
    )
    tweet = Tweet(**test_data)

    _db.session.add(tweet)
    _db.session.commit()

    resp = client.get('/api/load_previous_tweets')
    data = json.loads(resp.data)

    assert len(data['tweets']) == 1
    assert data['tweets'][0]['id'] == test_data['tweet_id']

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
