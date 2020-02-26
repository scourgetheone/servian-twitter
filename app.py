from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from google.cloud import ndb

import json

from twitter_streamer import create_new_stream, Tweet
from google_cloud import init_google_cloud_client, SystemConfig

app = Flask(__name__)

# Load up the json config file
with open('config.json') as f:
    CONFIG = json.load(f)
app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']

socketio = SocketIO(app)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev')
def index_dev():
    return render_template('index_dev.html')

@app.route('/load_previous_tweets')
def load_previous_tweets():
    """Loads previous tweets from Google Datastore"""
    with init_google_cloud_client().context():
        # First, get the stored config parameters from the Datastore
        DB_CONFIG = {
            config.key: config.value
            for config in SystemConfig.query()
        }
        TWEET_QUERY_LIMIT = DB_CONFIG['TWEET_QUERY_LIMIT'] or CONFIG['TWEET_QUERY_LIMIT'] or 100
        STREAM_KEYWORD = DB_CONFIG['TWITTER_STREAM_KEYWORD']

        query = Tweet.query(limit=STREAM_KEYWORD)\
            .filter(Tweet.stream_keyword == STREAM_KEYWORD)\
            .order(-Tweet.created_at)

        results = [{
            'created_at': tweet.created_at,
            'hashtags': tweet.hashtags,
            'text': tweet.text,
            'user': tweet.user,
            'user_loc': tweet.user_loc,
        } for tweet in query]

        return jsonify({
            'stream_keyword': STREAM_KEYWORD,
            'tweets': results
        }), 200

@app.route('/cron_create_streamer')
def create_streamer():
    # Initiate the real-time twitter stream
    with init_google_cloud_client().context():
        # First, get the stored config parameters from the Datastore
        DB_CONFIG = {
            config.key: config.value
            for config in SystemConfig.query()
        }
        STREAM_KEYWORD = DB_CONFIG['TWITTER_STREAM_KEYWORD']
        create_new_stream(STREAM_KEYWORD, on_receive_tweet)

# Socket.io functions
def on_receive_tweet(tweet):
    emit('here_are_tweets', tweet)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
