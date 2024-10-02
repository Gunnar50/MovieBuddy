import dataclasses


@dataclasses.dataclass
class UserMeta:
  id: str
  name: str
  email_address: str


@dataclasses.dataclass
class WatchlistMeta:
  name: str
  user_meta: UserMeta
