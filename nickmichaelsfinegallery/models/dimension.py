from google.appengine.ext import ndb

class Dimension (ndb.Model):
    """Models an individual Dimension entry"""
    cmLength = ndb.FloatProperty
    inchLength = ndb.FloatProperty
    footLength = ndb.FloatProperty
    mmLength = ndb.FloatProperty