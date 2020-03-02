from flask_sqlalchemy import SQLAlchemy

from servian_twitter import app
db = SQLAlchemy(app)

import json

# SQLite table definitions
class Tweet(db.Model):
    """Tweet entity stores basic information about a tweet"""
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String(256), nullable=False) # The tweet Id that comes from Twitter
    avatar_color_index = db.Column(db.Integer) # We generate a unique index for the UI's avatar display
    stream_keyword = db.Column(db.String(256)) # The keyword used in the stream that fetched this tweet
    created_at = db.Column(db.DateTime) # Datetime when the tweet was made. In UTC.
    hashtags = db.Column(db.String(512)) # A space-separated list of hashtags used in the tweet
    text = db.Column(db.Text) # The tweet content
    user = db.Column(db.String(256)) # The username
    user_loc = db.Column(db.String(256)) # The user's location

class SystemConfig(db.Model):
    """SystemConfig entity stores key value entities

    Useful for storing config parameters.
    """
    key = db.Column(db.String(512), primary_key=True)
    value = db.Column(db.String(512))
