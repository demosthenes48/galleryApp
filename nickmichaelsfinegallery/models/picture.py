from google.appengine.ext import ndb

class Picture (ndb.Model):
    """Models an individual Picture entry"""
    description = ndb.StringProperty(indexed=False)
    file_name = ndb.StringProperty(indexed=True)
    picture = ndb.BlobProperty(default=None)