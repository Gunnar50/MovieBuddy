import os

import flask
from google.appengine.api import wrap_wsgi_app

from utils import constants


def create_app() -> flask.Flask:
  flask_app = flask.Flask(
      __name__,
      template_folder='dist/browser',
      static_folder='dist/browser',
      static_url_path='',
  )
  # Ensure auto-escaping is always enabled
  flask_app.jinja_env.autoescape = True
  flask_app.wsgi_app = wrap_wsgi_app(flask_app.wsgi_app)
  flask_app.secret_key = os.urandom(24)

  return flask_app


def register_routes(flask_app: flask.Flask):
  from routes import auth
  from routes import general
  from routes import watchlists

  flask_app.register_blueprint(general.ROUTES)
  flask_app.register_blueprint(watchlists.ROUTES)
  flask_app.register_blueprint(auth.ROUTES)


app = create_app()
register_routes(app)

# For running concurrently (not through dev_appserver.py)
if constants.LOCAL_DEV:
  app.run(debug=True)
