from google.appengine.ext import ndb
from picture import Picture

class Category (ndb.Model):
    """Models an individual Category entry"""
    activeFlag = ndb.BooleanProperty
    categoryName = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=Picture)