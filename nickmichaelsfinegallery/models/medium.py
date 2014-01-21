from google.appengine.ext import ndb

class Medium (ndb.Model):
    """Models an individual Medium entry"""
    name = ndb.StringProperty(indexed=True)