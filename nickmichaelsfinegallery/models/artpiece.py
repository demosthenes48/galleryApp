from google.appengine.ext import ndb
from artist import Artist
from category import Category
from file import File

class ArtPiece (ndb.Model):
    """Models an individual ArtPiece entry"""
    activeFlag = ndb.BooleanProperty(default=True)
    artist = ndb.KeyProperty(kind=Artist)
    categories = ndb.KeyProperty(kind=Category, repeated=True)
    colors = ndb.StringProperty(indexed=True)
    depth = ndb.StringProperty(indexed=True)
    description = ndb.StringProperty(indexed=False)
    height = ndb.StringProperty(indexed=True)
    itemNumber = ndb.StringProperty(indexed=True)
    masterArtPiece = ndb.KeyProperty(kind='ArtPiece')
    masterArtFlag = ndb.BooleanProperty(default=False)
    mediums = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File)
    price = ndb.StringProperty(indexed=True)
    priceDisplay = ndb.StringProperty(indexed=False)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)
    weight = ndb.StringProperty(indexed=True)
    width = ndb.StringProperty(indexed=True)