from google.appengine.ext import ndb

class Color (ndb.Model):
    """Models an individual Color entry"""
    color = ndb.StringProperty(indexed=True)