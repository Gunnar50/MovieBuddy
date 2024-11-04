import enum

import pydantic


class LoginRequest(pydantic.BaseModel):
  access_token: str


class MemberType(enum.Enum):
  OWNER = 'owner'
  MEMBER = 'member'


class MemberDetail(pydantic.BaseModel):
  name: str
  email: str
  member_type: MemberType


class WatchlistDetail(pydantic.BaseModel):
  watchlist_id: int
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
  owner: int  # User profile ID
  members: list[str] = []  # List of emails


class WatchlistUpdateRequest(pydantic.BaseModel):
  name: str


class WatchlistRequest(pydantic.BaseModel):
  item_id: int


class MovieDetails(pydantic.BaseModel):
  pass
