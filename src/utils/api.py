import enum

import pydantic


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


class MovieDetails(pydantic.BaseModel):
  pass
