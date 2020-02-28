from flask import Blueprint, jsonify

from servian_twitter import app, socketio, CONFIG
from servian_twitter.twitter_streamer import create_new_stream
from servian_twitter import models
from servian_twitter.models import db
from servian_twitter import utils

bp = Blueprint('api', __name__, url_prefix='/api')

#### Flask routes ###

@bp.route('/load_previous_tweets')
def load_previous_tweets():
    """Loads previous tweets from SQLite

    https://app_url/load_previous_tweets
    """
    # First, get the stored config parameters from SQLite
    DB_CONFIG = utils.get_db_config()
    TWEET_QUERY_LIMIT = DB_CONFIG.get('TWEET_QUERY_LIMIT') or CONFIG.get('TWEET_QUERY_LIMIT') or 100
    TWEET_QUERY_LIMIT = int(TWEET_QUERY_LIMIT) if type(TWEET_QUERY_LIMIT) != int else TWEET_QUERY_LIMIT
    STREAM_KEYWORD = DB_CONFIG.get('TWITTER_STREAM_KEYWORD', 'hellow')

    query = models.Tweet.query\
        .filter(models.Tweet.stream_keyword == STREAM_KEYWORD)\
        .order_by(models.Tweet.created_at.desc())

    results = [{
        'id': tweet.tweet_id,
        'avatar_color_index': tweet.avatar_color_index,
        'created_at': utils.render_datetime(tweet.created_at),
        'hashtags': tweet.hashtags,
        'text': tweet.text,
        'user': tweet.user,
        'user_loc': tweet.user_loc,
    } for tweet in query.all()]

    return jsonify({
        'stream_keyword': STREAM_KEYWORD,
        'tweets': results
    }), 200


@bp.route('/cron_delete_all_tweets')
def delete_all_tweets():
    """Cron route to delete all tweets

    https://app_url/cron_delete_all_tweets
    """
    models.Tweet.query.delete()
    db.session.commit()
    return 'OK', 200

###  Setting up the Twitter streaming API ###
# The stream object.
stream = None

@bp.route('/cron_create_streamer')
def create_streamer():
    """Cron route to create the twitter stream object

    https://app_url/cron_create_streamer
    """

    global stream

    if not stream:
        # First, get the stored config parameters from SQLite
        DB_CONFIG = utils.get_db_config()
        STREAM_KEYWORD = DB_CONFIG.get('TWITTER_STREAM_KEYWORD', 'hello')

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

def on_error(status_code):
    """Handle errors from the stream object"""
    print ('There was an error with the Tweepy stream. Code: ', status_code)
    stream = None
    # Try to start a new stream
    create_streamer()

### Socket.io functions ###
def on_receive_tweet(tweet):
    """Emit tweet received event for the client listener"""
    tweet_dict = {
        'id': tweet.tweet_id,
        'avatar_color_index': tweet.avatar_color_index,
        'created_at': utils.render_datetime(tweet.created_at),
        'hashtags': tweet.hashtags,
        'text': tweet.text,
        'user': tweet.user,
        'user_loc': tweet.user_loc,
    }
    socketio.emit('here_are_tweets', tweet_dict)

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass

