from google.appengine.ext import ndb


class TrackedModel(ndb.Model):
  created_at = ndb.DateTimeProperty(auto_now_add=True)
  modified_at = ndb.DateTimeProperty(auto_now=True)


class User(TrackedModel):
  name = ndb.StringProperty(required=True)
  email_address = ndb.StringProperty(required=True)


class Watchlist(TrackedModel):
  title = ndb.StringProperty(required=True)
  description = ndb.StringProperty(required=True, default='')
  # IDs from the movie api
  items = ndb.IntegerProperty(repeated=True)
  watched_items = ndb.IntegerProperty(repeated=True)

  # Future?
  image = ndb.StringProperty()
  is_public = ndb.BooleanProperty(default=False)


class WatchlistOwner(TrackedModel):
  name = ndb.StringProperty(required=True)
  email = ndb.StringProperty(required=True)
  watchlist = ndb.KeyProperty(Watchlist, required=True)


class WatchlistMember(TrackedModel):
  name = ndb.StringProperty(required=True)
  email = ndb.StringProperty(required=True)
  watchlist = ndb.KeyProperty(Watchlist, required=True)
