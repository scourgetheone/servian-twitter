from servian_twitter import models
from servian_twitter import app

def render_datetime(datetime):
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def get_db_config():
    with app.app_context():
        return {
            config.key: config.value
            for config in models.SystemConfig.query.all()
        }
