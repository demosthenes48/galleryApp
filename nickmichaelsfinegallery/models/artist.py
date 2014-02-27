from google.appengine.ext import ndb
from file import File

class Artist (ndb.Model):
    """Models an individual Artist entry"""
    activeFlag = ndb.BooleanProperty
    biography = ndb.TextProperty
    firstName = ndb.StringProperty(indexed=True)
    lastName = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File)
