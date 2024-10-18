import dataclasses
import enum
import functools

from flask import json

from src.utils import exceptions
from src.utils import db_models
from google.oauth2 import id_token
from google.appengine.api import users
from google.auth.transport import requests
from src.utils import constants
from src.utils.services import secrets


@dataclasses.dataclass
class UserMeta:
  id: str
  name: str
  email: str
  is_owner: bool
  is_member: bool


class UserMetaType(enum.Enum):
  OWNER = 'owner'
  MEMBER = 'member'
  NONE = 'none'


@dataclasses.dataclass
class WatchlistMeta:
  user_meta: UserMeta
  watchlist: db_models.Watchlist


def requires_user(func):
  # Gets the user_meta

  @functools.wraps(func)
  def inner(*args, **kwargs):
    user_meta = get_user_meta()
    return func(user_meta=user_meta, *args, **kwargs)

  return inner


def requires_watchlist(user_types: tuple[UserMetaType, ...] = (
    UserMetaType.OWNER,
    UserMetaType.MEMBER,
)):

  def requires_watchlist_wrapper(func):
    # Watchlist must exist & user must have access

    @functools.wraps(func)
    def inner(*args, **kwargs):
      user_meta = get_user_meta()

      # Get the list & event
      watchlist = db_models.Watchlist.get_by_id(kwargs['list_id'])
      if not watchlist:
        raise exceptions.EntityNotFoundException

      user_type = _get_user_type(user_meta, watchlist)
      if user_type in user_types:
        list_meta = WatchlistMeta(user_meta=user_meta, watchlist=watchlist)
        return func(list_meta=list_meta, *args, **kwargs)
      else:
        raise exceptions.NoAccessException

    return inner

  return requires_watchlist_wrapper


def get_user_meta() -> UserMeta:
  current_user = users.get_current_user()

  if not current_user:
    raise exceptions.NotAuthenticatedException

  email = current_user.email()

  # Check the user own or is a member of the list
  is_owner = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.email == email).count() > 0

  is_member = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.email == email).count() > 0

  return UserMeta(
      id=current_user.user_id(),
      name=current_user.nickname,
      email=email,
      is_owner=is_owner,
      is_member=is_member,
  )


def _get_user_type(
    user_meta: UserMeta,
    watchlist: db_models.Watchlist,
) -> UserMetaType:
  if user_meta.is_owner:
    # Check if this user is a owner of this watchlist
    is_list_owner = db_models.WatchlistOwner.query(
        db_models.WatchlistOwner.email == user_meta.email,
        db_models.WatchlistOwner.watchlist == watchlist.key).count() > 0
    if is_list_owner:
      return UserMetaType.OWNER

  if user_meta.is_member:
    # Check if this user is a member of this watchlist
    is_list_member = db_models.WatchlistMember.query(
        db_models.WatchlistMember.email == user_meta.email,
        db_models.WatchlistMember.watchlist == watchlist.key).count() > 0
    if is_list_member:
      return UserMetaType.MEMBER

  # No access
  return UserMetaType.NONE


@dataclasses.dataclass
class UserInfo:
  id: str
  email_address: str
  name: str


def get_client_id() -> str:
  client_config = json.loads(secrets.get_secret(constants.SECRET_ID))
  return client_config['web']['client_id']


def login(token: str) -> UserInfo:
  client_id = get_client_id()
  try:
    id_info = id_token.verify_token(token,
                                    requests.Request(),
                                    audience=client_id)

    # Token is valid; extract user information
    user_info = UserInfo(id=id_info['sub'],
                         email_address=id_info['email'],
                         name=id_info.get('name'))
    return user_info
  except Exception:
    raise exceptions.EntityNotFoundException
