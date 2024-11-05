from utils import api
from utils import db_models


def serialise_watchlist_details(
    watchlist: db_models.Watchlist) -> api.WatchlistDetail:
  return api.WatchlistDetail(
      watchlist_id=watchlist.key.id(),
      title=watchlist.title,
      description=watchlist.description,
  )


def serialise_watchlist_response(
    watchlist: db_models.Watchlist,
    owner: db_models.WatchlistOwner,
    members: list[db_models.WatchlistMember],
) -> api.WatchlistResponse:
  sorted_members = sorted(members, key=lambda member: member.email)
  return api.WatchlistResponse(
      watchlist=serialise_watchlist_details(watchlist),
      owner=api.MemberDetail(
          email=owner.email,
          member_type=api.MemberType.OWNER,
      ),
      members=[
          api.MemberDetail(
              email=member.email,
              member_type=api.MemberType.MEMBER,
          ) for member in sorted_members
      ],
  )
