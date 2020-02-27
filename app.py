from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from google.cloud import ndb

import json

from twitter_streamer import create_new_stream, Tweet
from google_cloud import init_google_cloud_client, SystemConfig


### Initializations ###
app = Flask(__name__)

# Load up the json config file
with open('config.json') as f:
    CONFIG = json.load(f)
app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']

socketio = SocketIO(app)


#### Flask routes ###
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev')
def index_dev():
    return render_template('index_dev.html')

@app.route('/load_previous_tweets')
def load_previous_tweets():
    """Loads previous tweets from Google Datastore

    https://app_url/load_previous_tweets
    """
    with init_google_cloud_client().context():
        # First, get the stored config parameters from the Datastore
        DB_CONFIG = {
            config.key: config.value
            for config in SystemConfig.query()
        }
        TWEET_QUERY_LIMIT = int(DB_CONFIG['TWEET_QUERY_LIMIT']) or int(CONFIG['TWEET_QUERY_LIMIT']) or 100
        STREAM_KEYWORD = DB_CONFIG['TWITTER_STREAM_KEYWORD']

        query = Tweet.query()\
            .filter(Tweet.stream_keyword == STREAM_KEYWORD)\
            .order(-Tweet.created_at)

        results = [{
            'id': tweet.id,
            'avatar_color_index': tweet.avatar_color_index,
            'created_at': render_datetime(tweet.created_at),
            'hashtags': tweet.hashtags,
            'text': tweet.text,
            'user': tweet.user,
            'user_loc': tweet.user_loc,
        } for tweet in query.fetch(TWEET_QUERY_LIMIT)]

        return jsonify({
            'stream_keyword': STREAM_KEYWORD,
            'tweets': results
        }), 200


@app.route('/cron_delete_all_tweets')
def delete_all_tweets():
    """Cron route to delete all tweets

    https://app_url/cron_delete_all_tweets
    """
    with init_google_cloud_client().context():
        ndb.delete_multi(
            Tweet.query().fetch(keys_only=True)
        )
    return 'OK', 200

###  Setting up the Twitter streaming API ###
# The stream object.
stream = None

@app.route('/cron_create_streamer')
def create_streamer():
    """Cron route to create the twitter stream object

    https://app_url/cron_create_streamer
    """

    global stream

    if not stream:
        google_client = init_google_cloud_client()

        with google_client.context():
            # First, get the stored config parameters from the Datastore
            DB_CONFIG = {
                config.key: config.value
                for config in SystemConfig.query()
            }
            STREAM_KEYWORD = DB_CONFIG['TWITTER_STREAM_KEYWORD']

            stream = create_new_stream(
                STREAM_KEYWORD,
                return_object=True,
                on_receive_tweet=on_receive_tweet,
                on_error=on_error,
            )

            # Start the stream
            stream.filter(track=[STREAM_KEYWORD], is_async=True)
            return 'OK', 200
    else:
        print ('Twitter stream is already running, mate.')
        return 'OK', 200

def on_error():
    """Handle errors from the stream object"""
    pass



### Socket.io functions ###
def on_receive_tweet(tweet):
    """Emit tweet received event for the client listener"""
    tweet_dict = {
        'id': tweet.id,
        'avatar_color_index': tweet.avatar_color_index,
        'created_at': render_datetime(tweet.created_at),
        'hashtags': tweet.hashtags,
        'text': tweet.text,
        'user': tweet.user,
        'user_loc': tweet.user_loc,
    }
    socketio.emit('here_are_tweets', tweet_dict)

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass


### Util functions ###
def render_datetime(datetime):
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
