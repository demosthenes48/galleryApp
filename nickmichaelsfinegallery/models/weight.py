from google.appengine.ext import ndb

class Weight (ndb.Model):
    """Models an individual Weight entry"""
    kgWeight = ndb.FloatProperty
    lbWeight = ndb.FloatProperty