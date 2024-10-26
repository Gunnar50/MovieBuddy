import os

import cachetools
import flask
from google.auth.transport import requests
from google.oauth2 import id_token

from utils import constants
from utils.services import auth
from utils.services import secrets

ROUTES = flask.Blueprint('auth', __name__, url_prefix='/user/api/auth')


@ROUTES.route('/login', methods=('POST',))
def login():
  token = flask.request.json.get('token')
  if not token:
    return flask.jsonify({'error': 'No token provided'})

  user_info = auth.login(token)
  flask.session[constants.SESSION_USER_ID] = user_info.id
  flask.session['name'] = user_info.name

  return flask.jsonify({
      "message": "Login successful",
      "user_id": user_info.id,
      "email": user_info.email_address,
      "name": user_info.name,
      "success": True,
  })


@ROUTES.route("/logout", methods=('POST',))
def logout():
  # Clear the session
  flask.session.clear()
  return flask.redirect(flask.url_for('general.home'))
