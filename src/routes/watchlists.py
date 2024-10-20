import flask

from utils import db_models
from utils.services import auth

ROUTES = flask.Blueprint('watchlists', __name__, url_prefix='/user/api')


@ROUTES.route('/lists/')
@auth.requires_user
def list_all(user_meta: auth.UserMeta):
  # List all user lists
  owned_lists = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.email == user_meta.email).fetch()
  member_lists = db_models.WatchlistMember.query(
      db_models.WatchlistMember.email == user_meta.email).fetch()

  # for every list we need to fetch all members and owner to return a list of
  # watchlists containing all the watchlist info (title, owner, shared_with)


@ROUTES.route('/list/<int:watchlist_id>')
@auth.requires_watchlist(auth.UserMetaType.OWNER, auth.UserMetaType.MEMBER)
def list_details(watchlist_meta: auth.WatchlistMeta):
  # Get specific watchlist
  owner = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.watchlist == watchlist_meta.watchlist).get()

  members = db_models.WatchlistMember.query(
      db_models.WatchlistMember.watchlist == watchlist_meta.watchlist).fetch()
