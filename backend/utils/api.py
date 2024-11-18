import enum
from typing import Optional

import pydantic


class Config(pydantic.BaseModel):
  client_id: str


class UserDetails(pydantic.BaseModel):
  user_id: int
  email: str
  name: str


class LoginRequest(pydantic.BaseModel):
  access_token: str


class MemberType(enum.Enum):
  OWNER = 'owner'
  MEMBER = 'member'


class MemberDetail(pydantic.BaseModel):
  email: str
  member_type: MemberType


class WatchlistDetail(pydantic.BaseModel):
  title: str
  description: str


class WatchlistResponse(pydantic.BaseModel):
  watchlist: WatchlistDetail
  owner: MemberDetail
  members: list[MemberDetail]


class UserWatchlistsInfo(pydantic.BaseModel):
  watchlists: list[WatchlistResponse]


class WatchlistCreateRequest(pydantic.BaseModel):
  title: str
  description: str
  members: list[str] = []  # List of emails


class WatchlistUpdateRequest(pydantic.BaseModel):
  name: str


class WatchlistRequest(pydantic.BaseModel):
  item_id: int


class WatchlistItemRequest(pydantic.BaseModel):
  id: int
  title: str
  overview: str
  poster_path: Optional[str]
  genre_ids: list[int]
  release_date: Optional[str] = None
  first_air_date: Optional[str] = None
