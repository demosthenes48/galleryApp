from google.appengine.ext import ndb
from google.appengine.api import search
from file import File

class Category (ndb.Model):
    """Models an individual Category entry"""
    activeFlag = ndb.BooleanProperty
    categoryName = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)

    ''' #No longer needed because it needlessly uses up daily quota for simple search
    def add_to_search_index(self):
        fields = [
            search.TextField(name="categoryName", value=self.categoryName),
            search.TextField(name='suggest', value=self.build_suggestions())
        ]
        document = search.Document(doc_id=str(self.key.id()), fields=fields)
        index = search.Index(name='Category_index')
        index.put(document)

    def remove_from_search_index(self):
        index = search.Index(name='Category_index')
        index.delete(str(self.key.id()))

    def build_suggestions(self):
        suggestions = []
        string = self.categoryName
        for word in string.split():
            prefix = ""
            for letter in word:
                prefix += letter
                suggestions.append(prefix)
        return ' '.join(suggestions)
    '''