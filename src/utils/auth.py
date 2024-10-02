import dataclasses
import functools

from utils import exceptions


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
    watchlist = db_models.Watchlist_.get_by_id(kwargs['list_id'])
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
