[![Build Status](https://travis-ci.org/scourgetheone/servian-twitter.svg?branch=master)](https://travis-ci.org/scourgetheone/servian-twitter.svg?branch=master)

## Servian Real-time Twitter Stream Project

### Requirements
A client wants to build a web-based application (and relevant infrastructure) to showcase a stream of Twitter tweets to end-users in real-time.

### Introduction
The Servian real-time Twitter stream (ST) project is a web-based application built on Flask and React running on the GCP.

TODO: screenshot/gif here

### Architecture Overview

- The system config is stored in Datastored (previously in a json file). This is because we want to change the config on the fly
without having to change a file stored in the application server.

### Technology rationale
#### Front-end
Building a real-time web-based application immediately called out for "[_React!!_](https://reactjs.org/docs/getting-started.html)" in my mind, although true real-time communication between client-server has not been an area I am too familiar with. There is an option of using good'ol ajax to poll the web server every few seconds, but I wanted to explore something that handles "true" real-time communication. That is where I started exploring about websockets. Thus, [_socketio_](https://flask-socketio.readthedocs.io/en/latest/) with _eventlet_ (used by [_gunicorn_](https://gunicorn.org/) in App Engine) were chosen.

[_React Material UI_](https://material-ui.com/) was chosen as the styling boilerplate because it looks cool and makes styling and changing UI easy and has out-of-the-box responsiveness for different client device screen resolution, perfect for this web-based project.

[_Webpack_](https://webpack.js.org/) is used to package the React app into a single-page-application. [_Babel_](https://babeljs.io/) is used to get access to cutting-edge Javascript (ES6) and JSX. [_Eslint_](https://eslint.org/) is used for configurable javascript code quality control.

#### Back-end
[_Flask_](http://flask.palletsprojects.com/en/) is a very lightweight and flexible web framework, and thus was chosen exactly due to the scope of this project. It's flexibility also meant that if the project scope ever inflates to gigantic proportions, there is a plethora of python packages that will probably do the job well, like [handling database connections](https://www.sqlalchemy.org/), [building restful apis](https://flask-restful.readthedocs.io/en/latest/), or [doing cool stuff on the GCP](https://github.com/googleapis/google-api-python-client).

### Project folder structure

### Useful commands

Set the default GCP project:
> gcloud config set project hazel-tome-269200

Update the Datastore index:
> gcloud datastore indexes create index.yaml

### References

1. https://stackabuse.com/accessing-the-twitter-api-with-python/
2. https://flask-socketio.readthedocs.io/en/latest/
3. https://flask.palletsprojects.com/en/1.1.x/testing/
4. https://googleapis.dev/python/python-ndb/latest/index.html
5. https://material-ui.com/
6. https://reactjs.org/docs
