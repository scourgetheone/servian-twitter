import os
import pytest
import json
import datetime
import fnmatch

from servian_twitter import app

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
    CONFIG = json.load(f)

@pytest.fixture
def client():
    settings_override = {
        'TESTING': True,
    }

    # Establish an application context before running the tests.
    for key, value in settings_override.items():
        app.config[key] = value

    with app.test_client() as client:
        yield client

@pytest.mark.index_test
def test_get_index_page(client):
    """Make sure the index.html page loads"""

    rv = client.get('/')
    assert b'<title>Servian Real-time Tweet Stream</title>' in rv.data

def find(pattern, path):
    """Finds files matching pattern

    https://stackoverflow.com/a/1724723
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

@pytest.mark.index_test
def test_get_index_page_app_js(client):
    """Make sure the app.*.js file exists and index.html references it"""

    # Find the bundled react module file
    filename = find('app.*.js', 'static')
    rv = client.get('/')

    assert len(filename) == 1
    assert filename[0].split('static/')[1].encode() in rv.data

def test_get_dev_page(client):
    """Make sure the index_dev.html page loads"""

    rv = client.get('/dev')
    assert b'<title>Servian Real-time Tweet Stream</title>' in rv.data
    assert b'src="http://localhost:8080/app.js"' in rv.data
