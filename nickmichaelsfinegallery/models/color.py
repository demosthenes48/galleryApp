from google.appengine.ext import ndb

class Color (ndb.Model):
    """Models an individual color entry"""
    color = ndb.StringProperty(indexed=True)