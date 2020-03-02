from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

import json
import os

### Initializations ###
app = Flask(__name__)

# Load up the json config file
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
    CONFIG = json.load(f)
app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['SQLITE_URL']

socketio = SocketIO(app)

from servian_twitter.models import db
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev')
def index_dev():
    return render_template('index_dev.html')

from servian_twitter.api import bp
app.register_blueprint(bp)

@app.before_first_request
def execute_this():
    if not app.config['TESTING']:
        # Initiate the streamer
        from servian_twitter.api import create_streamer
        create_streamer()

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
