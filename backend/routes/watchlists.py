import collections
import email

import flask
# pip install appengine-python-standard
from google.appengine.ext import ndb

from utils import api
from utils import db_models
from utils.services import auth
from utils.services import flask_helpers
from utils.services import serialisers

ROUTES = flask.Blueprint('watchlists', __name__, url_prefix='/user/api')


@ROUTES.route('/watchlists/')
@auth.requires_any_watchlist
@flask_helpers.json_handler
def list_all(user_meta: auth.UserMeta) -> api.UserWatchlistsInfo:
  # Get all watchlists this user own
  watchlist_owner = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.email == user_meta.email).fetch()
  owned_lists_keys = [owner.watchlist for owner in watchlist_owner]

  # Get all watchlists this user is a member
  watchlist_member = db_models.WatchlistMember.query(
      db_models.WatchlistMember.email == user_meta.email).fetch()
  member_lists_keys = [member.watchlist for member in watchlist_member]

  # Get all watchlists
  all_lists = ndb.get_multi(owned_lists_keys + member_lists_keys)

  # Get all members for all lists that the user own and/or is a member of
  all_lists_owners = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.watchlist.IN(member_lists_keys)).fetch()
  all_lists_owners.extend(watchlist_owner)
  watchlist_owner_by_key: dict[
      ndb.Key,
      db_models.WatchlistOwner,
  ] = collections.defaultdict(db_models.WatchlistOwner)
  for owner in all_lists_owners:
    watchlist_owner_by_key[owner.watchlist] = owner

  # Get all members for all lists that the user own and/or is a member of
  all_lists_members = db_models.WatchlistMember.query(
      db_models.WatchlistMember.watchlist.IN(owned_lists_keys +
                                             member_lists_keys)).fetch()
  watchlist_member_by_key: dict[
      ndb.Key,
      list[db_models.WatchlistMember],
  ] = collections.defaultdict(list)
  for member in all_lists_members:
    watchlist_member_by_key[member.watchlist].append(member)

  sorted_watchists = sorted(all_lists, key=lambda watchlist: watchlist.title)

  return api.UserWatchlistsInfo(watchlists=[
      serialisers.serialise_watchlist_response(
          watchlist=watchlist,
          owner=watchlist_owner_by_key[watchlist.key],
          members=watchlist_member_by_key[watchlist.key],
      ) for watchlist in sorted_watchists
  ])


@ROUTES.route('/watchlist/<int:watchlist_id>/')
@auth.requires_watchlist()
@flask_helpers.json_handler
def list_details(watchlist_meta: auth.WatchlistMeta,
                 **kwargs) -> api.WatchlistResponse:
  # Get specific watchlist
  owner = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.watchlist == watchlist_meta.watchlist.key).get()

  members = db_models.WatchlistMember.query(
      db_models.WatchlistMember.watchlist ==
      watchlist_meta.watchlist.key).fetch()

  return serialisers.serialise_watchlist_response(
      watchlist=watchlist_meta.watchlist,
      owner=owner,
      members=members,
  )


@ROUTES.route('/watchlist/create/', methods=('POST',))
@auth.requires_user
@flask_helpers.json_handler
def create_watchlist(user_meta: auth.UserMeta) -> api.WatchlistResponse:
  body, _ = flask_helpers.get_parameters(api.WatchlistCreateRequest)
  to_put = []

  # Create the watchlist
  watchlist = db_models.Watchlist(
      title=body.title,
      description=body.description,
  )
  watchlist.put()

  # Create the owner
  owner = db_models.WatchlistOwner(email=user_meta.email,
                                   watchlist=watchlist.key)
  to_put.append(owner)

  # Create the members
  # TODO - Add limit of members per watchlist?
  members = [
      db_models.WatchlistMember(email=email, watchlist=watchlist.key)
      for email in body.members
  ]
  to_put.extend(members)

  ndb.put_multi(to_put)

  return serialisers.serialise_watchlist_response(
      watchlist=watchlist,
      owner=owner,
      members=members,
  )


@ROUTES.route('/watchlist/<int:watchlist_id>/add/')
@auth.requires_watchlist()
@flask_helpers.json_handler
def add_item(watchlist_meta: auth.WatchlistMeta, **kwargs):
  body, _ = flask_helpers.get_parameters(api.WatchlistItemRequest)


@ROUTES.route('/watchlists/<int:watchlist_id>/remove/')
@auth.requires_any_watchlist
@flask_helpers.json_handler
def remove_item(watchlist_meta: auth.WatchlistMeta, **kwargs):
  pass
