import pydantic


class MemberDetail(pydantic.BaseModel):
  name: str
  email_address: str


class ListInfo(pydantic.BaseModel):
  name: str
  owner_id: int
  shared: list[MemberDetail]


class ListsInfo(pydantic.BaseModel):
  lists: list[ListInfo]


class ListCreateRequest(pydantic.BaseModel):
  name: str
  owner: str
  shared: list[int] = []  # List of user_id


class ListUpdateRequest(pydantic.BaseModel):
  name: str


class ListRequest(pydantic.BaseModel):
  item_id: int


class MovieDetails(pydantic.BaseModel):
  pass
