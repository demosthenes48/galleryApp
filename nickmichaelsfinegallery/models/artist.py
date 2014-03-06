from google.appengine.ext import ndb
from file import File

class Artist (ndb.Model):
    """Models an individual Artist entry"""
    activeFlag = ndb.BooleanProperty(default=True)
    biography = ndb.TextProperty(indexed=False)
    firstName = ndb.StringProperty(indexed=True, required=True)
    lastName = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File, required=True)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)
