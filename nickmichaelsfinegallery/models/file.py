from google.appengine.ext import ndb
from google.appengine.ext import blobstore

class File (ndb.Model):
    """Models an individual Picture or Video file entry"""
    blob = ndb.BlobKeyProperty(required=True)
    file_name = ndb.StringProperty(required=True, indexed=True)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)
    url = ndb.StringProperty(required=False)
    thumbnail = ndb.StringProperty(required=False)