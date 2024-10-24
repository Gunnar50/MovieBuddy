import enum
import pydantic


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
  name: str
  owner: str
  shared: list[int] = []  # List of user_id


class WatchlistUpdateRequest(pydantic.BaseModel):
  name: str


class WatchlistRequest(pydantic.BaseModel):
  item_id: int


class MovieDetails(pydantic.BaseModel):
  pass
