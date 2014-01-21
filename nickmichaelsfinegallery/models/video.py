from google.appengine.ext import ndb

class Video (ndb.Model):
    """Models an individual Video entry"""
    video = ndb.BlobProperty(default=None)
    videoName = ndb.StringProperty(indexed=False)