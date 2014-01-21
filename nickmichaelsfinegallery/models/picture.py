from google.appengine.ext import ndb

class Picture (ndb.Model):
    """Models an individual Picture entry"""
    picture = ndb.BlobProperty(default=None)
    pictureName = ndb.StringProperty(indexed=False)