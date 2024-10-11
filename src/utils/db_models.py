from google.appengine.ext import ndb


class TrackedModel(ndb.Model):
  created_at = ndb.DateTimeProperty(auto_now_add=True)
  modified_at = ndb.DateTimeProperty(auto_now=True)


# class Watchlist(TrackedModel):
#   name = ndb.StringProperty(required=True)
#   description = ndb.StringProperty(required=True)
#   created_by = ndb.IntegerProperty(required=True)  # User id
#   items = ndb.KeyProperty(Media, required=True)  # Array?
#   watched_items = ndb.KeyProperty(Media, required=True)  # Array?
#   image = ndb.StringProperty()

#   total_members = ndb.IntegerProperty(default=0)
#   is_public = ndb.BooleanProperty(default=False)

# - Name: string
# - description: string
# - created_by: string (user id)
# - shared: list of user ids
# - items: list of media ids
# - watched_Items: list of media ids
# - image: string (optional)
# - Public: boolean (default to false) (future)


class User(TrackedModel):
  email_address = ndb.StringProperty(required=True)
  # watchlist = ndb.KeyProperty(Watchlist, required=True)  # Array?
