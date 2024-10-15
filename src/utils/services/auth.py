import dataclasses
import functools

from flask import json

from src.utils import exceptions
from src.utils import db_models
from google.oauth2 import id_token

from google.auth.transport import requests
from src.utils import constants
from src.utils.services import secrets


@dataclasses.dataclass
class UserMeta:
  id: str
  name: str
  email_address: str


@dataclasses.dataclass
class WatchlistMeta:
  name: str
  user_meta: UserMeta


def requires_user(func):
  # Gets the user_meta

  @functools.wraps(func)
  def inner(*args, **kwargs):
    user_meta = get_user_meta()
    return func(user_meta=user_meta, *args, **kwargs)

  return inner


def requires_watchlist(func):
  # List must exist & user must have access

  @functools.wraps(func)
  def inner(*args, **kwargs):
    user_meta = get_user_meta()

    # Get the list & event
    watchlist = db_models.Watchlist.get_by_id(kwargs['list_id'])
    if not watchlist:
      raise exceptions.EntityNotFoundException

    # Check the user has access
    if user_type in user_types:
      list_meta = WatchlistMeta(user_meta=user_meta, event=event, list_=list_)
      return func(list_meta=list_meta, *args, **kwargs)
    else:
      raise exceptions.NoAccessException

  return inner


def get_user_meta() -> UserMeta:
  current_user = users.get_current_user()

  if not current_user:
    raise exceptions.NotAuthenticatedException

  email = current_user.email()

  return UserMeta(
      id=current_user.user_id(),
      email=email,
      name=nickname,
  )


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
    raise exceptions.EntityNotFound
