from servian_twitter import models
from servian_twitter import app

def render_datetime(datetime):
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def get_db_config():
    """Get the configuration from the SQLite database

        Returns:
            A dictionary of keys and values mapped from the models.SystemConfig table
    """
    with app.app_context():
        return {
            config.key: config.value
            for config in models.SystemConfig.query.all()
        }
