import flask

from utils import auth

ROUTES = flask.Blueprint('lists', __name__, url_prefix='/user/api')


@ROUTES.route('/lists/<int:user_id>/all')
def list_all(user_meta: auth.UserMeta):
  # List all user lists
  pass
