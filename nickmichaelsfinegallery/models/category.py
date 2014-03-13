from google.appengine.ext import ndb
from file import File

class Category (ndb.Model):
    """Models an individual Category entry"""
    activeFlag = ndb.BooleanProperty
    categoryName = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)