from twython import TwythonStreamer

from google_cloud import (
    Tweet,
    SystemConfig,
    init_google_cloud_client
)


# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):
    """A custom Twitter streamer class inherited from TwythonStreamer

    MyStreamer.__init__():

        Args:
            google_client (ndb.Client): the Google Cloud Client object
            stream_keyword (str): a keyword that we are tracking using the TwythonStreamer
            on_receive_tweet (func): a callback function used when a tweet matching the
            stream keyword is received.

    """

    on_receive_tweet = None
    stream_keyword = None
    google_client = None

    def __init__(self, google_client, stream_keyword, *args, on_receive_tweet=lambda x: None, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_keyword = stream_keyword
        self.on_receive_tweet = on_receive_tweet
        self.google_client = google_client

    # Filter out unwanted data
    def process_tweet(self, tweet):
        tweet_entity = Tweet(
            stream_keyword = self.stream_keyword,
            created_at = tweet['created_at'],
            hashtags = ' '.join([hashtag['text'] for hashtag in tweet['entities']['hashtags']]),
            text = tweet['text'],
            user = tweet['user']['screen_name'],
            user_loc = tweet['user']['location'],
        )
        return tweet_entity

    # Received data
    def on_success(self, data):
        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet = self.process_tweet(data)
            self.save_to_datastore(tweet)
            self.on_receive_tweet(tweet)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        # Uncomment if we want to stop retrying
        # self.disconnect()

    # Save each tweet to Google's Datastore
    def save_to_datastore(self, tweet):
        tweet.put()

REQUIRED_PARAMS = ['TWITTER_API_KEY', 'TWITTER_API_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_SECRET']

def create_new_stream(google_client, keyword_to_track, on_receive_tweet=lambda x: None):
    """ Create a new Twitter stream listener

    Args:
        keyword_to_track (str): the keyword to track with our Twitter streamer
        on_receive_tweet (func): a callback function when a real-time tweet is received

    """

    with google_client.context():
        # Load the system config from Google Datastore to
        # get our twitter config parameters
        DB_CONFIG = {
            config.key: config.value
            for config in SystemConfig.query()
        }

        for required_param in REQUIRED_PARAMS:
            assert DB_CONFIG[required_param], "{} is needed. Please add it to the \
                SystemConfig kind in the Google Datastore".format(required_param)

        # Instantiate from our streaming class
        stream = MyStreamer(client, keyword_to_track,
            DB_CONFIG['TWITTER_API_KEY'], DB_CONFIG['TWITTER_API_SECRET'],
            DB_CONFIG['TWITTER_ACCESS_TOKEN'], DB_CONFIG['TWITTER_ACCESS_SECRET'],
            on_receive_tweet=on_receive_tweet)

        # Start the stream
        stream.statuses.filter(track=keyword_to_track)


if __name__ == '__main__':
    client = init_google_cloud_client()

    with client.context():
        # Load the system config from Google Datastore to
        # get our twitter config parameters
        DB_CONFIG = {
            config.key: config.value
            for config in SystemConfig.query()
        }

    create_new_stream(client, DB_CONFIG['TWITTER_STREAM_KEYWORD'])
