from google.cloud import ndb
from google.oauth2 import service_account

import json

# Google Datastore Entity definitions
class Tweet(ndb.Model):
    """Tweet entity stores basic information about a tweet"""
    id = ndb.StringProperty()
    avatar_color_index = ndb.IntegerProperty() # We generate a unique index for the UI's avatar display
    stream_keyword = ndb.StringProperty() # The keyword used in the stream that fetched this tweet
    created_at = ndb.DateTimeProperty() # Datetime when the tweet was made (converted to UTC)
    hashtags = ndb.StringProperty() # A space-separated list of hashtags used in the tweet
    text = ndb.StringProperty() # The tweet content
    user = ndb.StringProperty() # The username
    user_loc = ndb.StringProperty() # The user's location

class SystemConfig(ndb.Model):
    """SystemConfig entity stores key value entities

    Useful for storing config parameters.

    """
    key = ndb.StringProperty()
    value = ndb.StringProperty()


def init_google_cloud_client():
    credentials = service_account.Credentials.from_service_account_file(
        'google-app-engine-creds.json')
    with open('config.json') as file:
        CONFIG = json.load(file)
    return ndb.Client(project=CONFIG['GCP_PROJECT_ID'], credentials=credentials)
