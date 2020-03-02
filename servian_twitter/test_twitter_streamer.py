import os
import pytest
import json

from servian_twitter import app, socketio
from servian_twitter.models import db, Tweet, SystemConfig
from servian_twitter.init_db import init_db
from servian_twitter.twitter_streamer import ServianTwitterStreamer

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


class MockTweet():
    _json = dict()

    def __init__(self, _dict):
        self._json = _dict

    def __getattr__ (self, key):
        return self._json[key]


def test_receive_tweet(_db, client):
    """Mock test receiving of a tweet from Twitter's API

    This also tests adding a new tweet to the database (via on_status)
    """

    # connect to Socket.IO
    socketio_test_client = socketio.test_client(
        app, flask_test_client=client)

    # make sure the server accepted the connection
    r = socketio_test_client.is_connected()
    assert r == True

    def on_receive_tweet(tweet):
        socketio.emit('here_are_tweets', tweet)

    # Create the ServianTwitterStreamer object
    stream_listener = ServianTwitterStreamer(
        'python',
        on_receive_tweet,
    )

    mock_tweet_data = MockTweet({
        "created_at": "Thu Feb 27 07:02:39 +0000 2020",
        "lang": "en",
        "id": 456456456,
        "text": "Test tweet text",
        "user": {
            "id": 1158415731861540865,
            "name": "Test user",
            "screen_name": "testuser",
            "location": None},
        "entities": {
            "hashtags": [
                {"text": "hashtag"}
            ]
        }
    })

    # Mock a tweet received event
    stream_listener.on_status(mock_tweet_data)

    # After the tweet is received, the socketio.emit() event
    # will be called. Get the event message
    r = socketio_test_client.get_received()

    # Check that the message content is consistent
    assert len(r) == 1
    # r[0]['args'][0] is a models.Tweet object
    assert r[0]['args'][0].tweet_id == str(mock_tweet_data.id)
