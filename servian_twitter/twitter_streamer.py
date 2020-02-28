
from pytz import timezone

import tweepy
import datetime
import random

from servian_twitter import utils
from servian_twitter.models import db
import servian_twitter.models as models

class ServianTwitterStreamer(tweepy.StreamListener):
    """A custom Twitter streamer class inherited from tweepy.StreamListener

    ServianTwitterStreamer.__init__():

        Args:
            stream_keyword (str): a keyword that we are tracking using the StreamListener
            on_receive_tweet (func): a callback function used when a tweet matching the
            stream keyword is received.

    """

    on_receive_tweet = None
    stream_keyword = None

    def __init__(self,
        stream_keyword,
        on_receive_tweet=lambda x: None,
        on_error=lambda x: None,
        ):
        super().__init__()
        self.stream_keyword = stream_keyword
        self.on_receive_tweet = on_receive_tweet
        self.on_error = on_error

    # Received data
    def on_status(self, data):
        data = data._json

        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet = self.process_tweet(data)
            self.save_to_database(tweet)
            self.on_receive_tweet(tweet)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.on_error(status_code, data)
        # uncomment if we do *not* want to retry the stream
        #self.disconnect()

    def process_tweet(self, tweet):
        """Filter out unwanted data from a tweet

            Args:
                tweet: a dictionary containing information about a tweet
        """
        # Parse the date time string with '%a %b %d %H:%M:%S %z %Y' format.
        # #Example date time from twitter: Wed Feb 26 00:13:42 +0000 2020
        created_at = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        # Convert to UTC aware then naive datetime for Google Datastore's DateTimeProperty
        created_at = created_at.astimezone(timezone('UTC')).replace(tzinfo=None)

        avatar_color_index = random.randint(0, 12)

        tweet_entity = models.Tweet(
            tweet_id = str(tweet['id']),
            avatar_color_index = avatar_color_index,
            stream_keyword = self.stream_keyword,
            created_at = created_at,
            hashtags = ' '.join([hashtag['text'] for hashtag in tweet['entities']['hashtags']]),
            text = tweet['text'],
            user = tweet['user']['screen_name'],
            user_loc = tweet['user']['location'],
        )
        return tweet_entity

    # Save each tweet to the database
    def save_to_database(self, tweet):
        db.session.add(tweet)
        db.session.commit()

REQUIRED_PARAMS = ['TWITTER_API_KEY', 'TWITTER_API_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_SECRET']

def create_new_stream(
        keyword_to_track,
        return_object=False,
        on_receive_tweet=lambda x: None,
        on_error=lambda x: None):
    """ Create a new Twitter stream listener

    Args:
        keyword_to_track (str): the keyword to track with our Twitter streamer
        return_object (bool): returns the ServianTwitterStreamer object instead of running the stream
        on_receive_tweet (func): a callback function when a real-time tweet is received
        on_error (func): a callback function when there is an error from the stream API

    """

    # Load the system config from Google Datastore to
    # get our twitter config parameters
    DB_CONFIG = utils.get_db_config()

    for required_param in REQUIRED_PARAMS:
        assert DB_CONFIG[required_param], "{} is needed. Please add it to the \
            models.SystemConfig table".format(required_param)

    auth = tweepy.OAuthHandler(DB_CONFIG['TWITTER_API_KEY'], DB_CONFIG['TWITTER_API_SECRET'])
    auth.set_access_token(DB_CONFIG['TWITTER_ACCESS_TOKEN'], DB_CONFIG['TWITTER_ACCESS_SECRET'])

    # Instantiate from our streaming class
    stream_listener = ServianTwitterStreamer(
        keyword_to_track,
        on_receive_tweet,
        on_error,
    )
    stream = tweepy.Stream(auth=auth, listener=stream_listener)

    if return_object:
        return stream
    else:
        # Start the stream
        stream.filter(track=[keyword_to_track], is_async=True)


if __name__ == '__main__':
    # Load the system config from Google Datastore to
    # get our twitter config parameters
    DB_CONFIG = utils.get_db_config()

    create_new_stream(DB_CONFIG['TWITTER_STREAM_KEYWORD'])
