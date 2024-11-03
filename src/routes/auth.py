import flask

from utils import api
from utils import constants
from utils import db_models
from utils.services import auth
from utils.services import flask_helpers

ROUTES = flask.Blueprint('auth', __name__, url_prefix='/user/api/auth')


@ROUTES.route('/login', methods=('POST',))
@flask_helpers.json_handler
def login():
  body, _ = flask_helpers.get_parameters(api.LoginRequest)
  # token = flask.request.json.get('token')
  user_info = auth.login(body.access_token)

  user_profile = db_models.UserProfile.get_by_id(user_info.google_id)
  if not user_profile:
    new_user = db_models.UserProfile(id=user_info.google_id,
                                     email_address=user_info.email_address,
                                     name=user_info.name,
                                     avatar=user_info.avatar)
    new_user.put()

  flask.session[constants.SESSION_USER_ID] = user_info.google_id

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
