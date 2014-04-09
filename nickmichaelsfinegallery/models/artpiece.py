from google.appengine.ext import ndb
from google.appengine.api import search

from artist import Artist
from category import Category
from file import File

class ArtPiece (ndb.Model):
    """Models an individual ArtPiece entry"""
    activeFlag = ndb.BooleanProperty(default=True)
    artist = ndb.KeyProperty(kind=Artist)
    categories = ndb.KeyProperty(kind=Category, repeated=True)
    colors = ndb.StringProperty(indexed=True)
    depth = ndb.StringProperty(indexed=True)
    description = ndb.StringProperty(indexed=False)
    height = ndb.StringProperty(indexed=True)
    itemNumber = ndb.StringProperty(indexed=True)
    masterArtPiece = ndb.KeyProperty(kind='ArtPiece')
    masterArtFlag = ndb.BooleanProperty(default=False)
    slaveArtFlag = ndb.BooleanProperty(default=False)
    mediums = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    picture = ndb.KeyProperty(kind=File)
    price = ndb.StringProperty(indexed=True)
    priceDisplay = ndb.StringProperty(indexed=False)
    uploaded_at = ndb.DateTimeProperty(required=True, auto_now=True)
    uploaded_by = ndb.UserProperty(required=True)
    weight = ndb.StringProperty(indexed=True)
    width = ndb.StringProperty(indexed=True)

    def add_to_search_index(self):
        categoriesString = self.categoryNames().replace(',', '')
        fields = [
            search.TextField(name="itemNumber", value=self.itemNumber),
            search.TextField(name="name", value=self.name),
            search.TextField(name='suggest', value=self.build_suggestions()),
            search.TextField(name='categories', value=categoriesString)
        ]
        document = search.Document(doc_id=str(self.key.id()), fields=fields)
        index = search.Index(name='ArtPiece_index')
        index.put(document)

    def remove_from_search_index(self):
        index = search.Index(name='ArtPiece_index')
        index.delete(str(self.key.id()))

    def build_suggestions(self):
        suggestions = []
        string = self.itemNumber + " " + self.name

        artist = self.artist.get()
        string += " " + artist.firstName + " " + artist.lastName

        for word in string.split():
            prefix = ""
            for letter in word:
                prefix += letter
                suggestions.append(prefix)
        return ' '.join(suggestions)

    def categoryNames(self):
        #return a comma separated list of categories
        categories = ndb.get_multi(self.categories)

        categoryNamesList = []
        for category in categories:
            categoryNamesList.append(str(category.categoryName))
        categoryNamesString = ", ".join(categoryNamesList)

        return categoryNamesString