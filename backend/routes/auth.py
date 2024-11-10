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
  # TODO - Update user profile in case something has changed.
  if not user_profile:
    db_models.UserProfile(
        id=user_info.google_id,
        email_address=user_info.email_address,
        name=user_info.name,
        avatar=user_info.avatar,
    ).put()

  flask.session[constants.SESSION_USER_ID] = user_info.google_id

  return api.UserDetails(
      user_id=user_info.google_id,
      email=user_info.email_address,
      name=user_info.name,
  )


@ROUTES.route('/logout', methods=('POST',))
@auth.requires_user
def logout(user_meta: auth.UserMeta) -> str:
  auth.logout()
  return 'Ok'
