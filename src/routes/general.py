import flask

from src.utils import db_models

ROUTES = flask.Blueprint('general', __name__)


@ROUTES.route('/_ah/warmup')
def warmup() -> str:
  # Nothing to do, just to make sure Flask etc. is ready to serve requests
  return 'Warmup complete!'


@ROUTES.route('/')
def home() -> str:
  return flask.render_template('index.html')


@ROUTES.route('/add')
def test_route() -> str:
  user = db_models.User(email_address='test@test.com').put()
  print(user)
  return flask.render_template('index.html')
