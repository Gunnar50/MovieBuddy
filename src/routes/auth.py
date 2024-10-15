import os
import cachetools
import flask
from google.oauth2 import id_token
from google.auth.transport import requests
from src.utils import constants
from src.utils.services import secrets
from src.utils.services import auth

ROUTES = flask.Blueprint('auth', __name__, url_prefix='/user/api/auth')


@ROUTES.route('/login', methods=('POST',))
def login():
  token = flask.request.json.get('token')
  if not token:
    return flask.jsonify({'error': 'No token provided'}), 400

  user_info = auth.login(token)
  # flask.session[constants.SESSION_USER_ID] = user_info.id

  return flask.jsonify({
      "message": "Login successful",
      "user_id": user_info.id,
      "email": user_info.email_address,
      "name": user_info.name,
  })


@ROUTES.route("/logout")
def logout():
  # Clear the session
  flask.session.pop(constants.SESSION_USER_ID)
  return flask.redirect(flask.url_for('index'))
