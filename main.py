import os
import flask
from src.utils import constants
from google.appengine.api import wrap_wsgi_app


def create_app() -> flask.Flask:
  flask_app = flask.Flask(__name__,
                          template_folder='src/templates',
                          static_folder='src/static/compiled')
  flask_app.wsgi_app = wrap_wsgi_app(flask_app.wsgi_app)
  flask_app.secret_key = os.urandom(24)
  return flask_app


def register_routes(flask_app: flask.Flask):
  from src.routes import general
  from src.routes import auth

  flask_app.register_blueprint(general.ROUTES)
  flask_app.register_blueprint(auth.ROUTES)


app = create_app()
register_routes(app)

# For running concurrently (not through dev_appserver.py)
if constants.LOCAL_DEV:
  app.run(debug=True)
