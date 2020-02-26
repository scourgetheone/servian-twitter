from google.cloud import ndb
from google.oauth2 import service_account

import json

# Google Datastore Entity definitions
class Tweet(ndb.Model):
    """Tweet entity stores basic information about a tweet"""
    stream_keyword = ndb.StringProperty()
    created_at = ndb.StringProperty()
    hashtags = ndb.StringProperty()
    text = ndb.StringProperty()
    user = ndb.StringProperty()
    user_loc = ndb.StringProperty()

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
