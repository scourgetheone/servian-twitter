#!/bin/bash
#
# start_server.sh: This script initializes the database
# and then starts the Flask web server.
#

# test and bundle the react app in production mode.
pushd servian_twitter/ >/dev/null
python init_db.py from_template
popd >/dev/null

if [ -z ${PORT+x} ]; then
    PORT=5000
fi

gunicorn -b :$PORT -k eventlet servian_twitter:app
