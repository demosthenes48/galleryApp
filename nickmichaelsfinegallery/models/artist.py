from google.appengine.ext import ndb
from google.appengine.api import search
from file import File

class Artist (ndb.Model):
    """Models an individual Artist entry"""
    activeFlag = ndb.BooleanProperty(default=True)
    biography = ndb.TextProperty(indexed=False)
    firstName = ndb.StringProperty(indexed=True, required=True)
    lastName = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File, required=True)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)

    ''' #No longer needed because we really want to search for art by this artist, category, etc...
    def add_to_search_index(self):
        fields = [
            search.TextField(name="firstName", value=self.firstName),
            search.TextField(name="lastName", value=self.lastName),
            search.TextField(name='suggest', value=self.build_suggestions())
        ]
        document = search.Document(doc_id=str(self.key.id()), fields=fields)
        index = search.Index(name='Artist_index')
        index.put(document)

    def remove_from_search_index(self):
        index = search.Index(name='Artist_index')
        index.delete(str(self.key.id()))

    def build_suggestions(self):
        suggestions = []
        string = self.firstName + " " + self.lastName
        for word in string.split():
            prefix = ""
            for letter in word:
                prefix += letter
                suggestions.append(prefix)
        return ' '.join(suggestions)
    '''
