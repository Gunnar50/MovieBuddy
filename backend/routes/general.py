import flask

from utils import db_models
from utils import api
from utils.services import auth
from utils.services import flask_helpers

ROUTES = flask.Blueprint('general', __name__)


@ROUTES.route('/_ah/warmup')
def warmup() -> str:
  # Nothing to do, just to make sure Flask etc. is ready to serve requests
  return 'Warmup complete!'


@ROUTES.route('/api/config')
@flask_helpers.json_handler
def get_config() -> api.ConfigResponse:
  client_id = auth.get_client_id()
  return api.ConfigResponse(client_id=client_id)


@ROUTES.route("/logged_in")
@auth.requires_user
def logged_in():
  # Check if user is logged in
  if 'user_id' not in flask.session:
    return flask.redirect(flask.url_for('general.home'))

  return flask.render_template("index.html", name=flask.session['name'])


# @ROUTES.route('/add')
# def test_route() -> str:
#   user = db_models.User(email_address='test@test.com').put()
#   print(user)
#   return flask.render_template('index.html')
