from google.appengine.ext import ndb
from artist import Artist
from dimension import Dimension
from category import Category
from color import Color
from medium import Medium
from file import File
from weight import Weight

class ArtPiece (ndb.Model):
    """Models an individual ArtPiece entry"""
    activeFlag = ndb.BooleanProperty
    artist = ndb.KeyProperty(kind=Artist)
    categories = ndb.KeyProperty(kind=Category, repeated=True)
    color = ndb.KeyProperty(kind=Color, repeated=True)
    depth = ndb.KeyProperty(kind=Dimension)
    description = ndb.StringProperty(indexed=False)
    height = ndb.KeyProperty(kind=Dimension)
    itemNumber = ndb.StringProperty(indexed=True)
    masterArtPiece = ndb.KeyProperty(kind='ArtPiece')
    masterArtFlag = ndb.BooleanProperty
    medium = ndb.KeyProperty(kind=Medium, repeated=True)
    name = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File)
    price = ndb.FloatProperty
    weight = ndb.KeyProperty(kind=Weight)
    width = ndb.KeyProperty(kind=Dimension)