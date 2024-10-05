import flask
from src.utils import constants


def create_app() -> flask.Flask:
  flask_app = flask.Flask(__name__,
                          template_folder='src/templates',
                          static_folder='src/static/compiled')
  return flask_app


def register_routes(flask_app: flask.Flask):
  from src.routes import general

  flask_app.register_blueprint(general.ROUTES)


app = create_app()
register_routes(app)

# For running concurrently (not through dev_appserver.py)
# app.run(debug=True)
