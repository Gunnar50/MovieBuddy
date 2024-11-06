import dataclasses
import enum
import functools
from typing import Optional

import flask
from flask import json
from google.appengine.api import users
from google.auth.transport import requests
from google.oauth2 import id_token

from utils import constants
from utils import db_models
from utils import exceptions
from utils.services import secrets


@dataclasses.dataclass
class UserMeta:
  id: str
  name: str
  email: str
  has_watchlists: bool


class UserMetaType(enum.Enum):
  OWNER = 'owner'
  MEMBER = 'member'
  NONE = 'none'


@dataclasses.dataclass
class WatchlistMeta:
  user_meta: UserMeta
  watchlist: db_models.Watchlist


def requires_user(func):
  # Gets the user_meta, user must be logged in

  @functools.wraps(func)
  def inner(*args, **kwargs):
    user_id = _get_user_id()
    user_meta = get_user_meta(user_id)
    return func(user_meta=user_meta, *args, **kwargs)

  return inner


def requires_any_watchlist(func):
  # Gets the user_meta, user must be owner or member of a watchlist

  @functools.wraps(func)
  def inner(*args, **kwargs):
    user_id = _get_user_id()
    user_meta = get_user_meta(user_id)
    if user_meta.has_watchlists:
      return func(user_meta=user_meta, *args, **kwargs)
    else:
      raise exceptions.NoAccessException

  return inner


def requires_watchlist(user_types: tuple[UserMetaType, ...] = (
    UserMetaType.OWNER,
    UserMetaType.MEMBER,
)):

  def requires_watchlist_wrapper(func):
    # Watchlist must exist & user must have access

    @functools.wraps(func)
    def inner(*args, **kwargs):
      user_id = _get_user_id()
      user_meta = get_user_meta(user_id)

      # Get the watchlist
      watchlist = db_models.Watchlist.get_by_id(kwargs['watchlist_id'])
      if not watchlist:
        raise exceptions.EntityNotFoundException

      user_type = _get_user_type(user_meta, watchlist)
      if user_type in user_types:
        watchlist_meta = WatchlistMeta(user_meta=user_meta, watchlist=watchlist)
        return func(watchlist_meta=watchlist_meta, *args, **kwargs)
      else:
        raise exceptions.NoAccessException

    return inner

  return requires_watchlist_wrapper


def _get_user_id() -> str:
  if user_id := flask.session.get(constants.SESSION_USER_ID):
    return user_id
  else:
    raise exceptions.MissingSessionCookieException


def get_user_meta(user_id: Optional[str]) -> UserMeta:
  if not user_id:
    raise exceptions.MissingSessionCookieException

  user_profile = db_models.UserProfile.get_by_id(user_id)
  if not user_profile:
    logout()
    raise exceptions.InvalidAuthenticationException

  # Check the user own and/or is a member of a list
  is_owner = db_models.WatchlistOwner.query(
      db_models.WatchlistOwner.email == user_profile.email_address).count() > 0

  is_member = db_models.WatchlistMember.query(
      db_models.WatchlistMember.email == user_profile.email_address).count() > 0

  return UserMeta(
      id=user_id,
      name=user_profile.name,
      email=user_profile.email_address,
      has_watchlists=is_owner or is_member,
  )


def _get_user_type(
    user_meta: UserMeta,
    watchlist: db_models.Watchlist,
) -> UserMetaType:
  if user_meta.has_watchlists:
    # Check if this user is a owner of this watchlist
    is_list_owner = db_models.WatchlistOwner.query(
        db_models.WatchlistOwner.email == user_meta.email,
        db_models.WatchlistOwner.watchlist == watchlist.key).get()
    if is_list_owner:
      return UserMetaType.OWNER

    # Check if this user is a member of this watchlist
    is_list_member = db_models.WatchlistMember.query(
        db_models.WatchlistMember.email == user_meta.email,
        db_models.WatchlistMember.watchlist == watchlist.key).get()
    if is_list_member:
      return UserMetaType.MEMBER

  # No access
  return UserMetaType.NONE


@dataclasses.dataclass
class UserInfo:
  google_id: int
  email_address: str
  name: str
  avatar: Optional[str]


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
    user_info = UserInfo(google_id=id_info['sub'],
                         email_address=id_info['email'],
                         name=id_info.get('name'),
                         avatar=id_info.get('picture'))
    return user_info
  except Exception:
    raise exceptions.EntityNotFoundException


def logout() -> None:
  flask.session.pop(constants.SESSION_USER_ID)
