from google.appengine.ext import ndb

class Medium (ndb.Model):
    """Models an individual color entry"""
    medium = ndb.StringProperty(indexed=True)