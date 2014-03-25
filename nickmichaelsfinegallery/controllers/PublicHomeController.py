import webapp2
import jinja2
import os
import logging

from models.artpiece import ArtPiece
from models.artpiece import Artist
from models.category import Category
from models.file import File

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicHome.html')

        photos = {}
        categories = Category.query().order(Category.categoryName)

        for category in categories:
            photos[category.key] = category.picture.get()

        templateVars = {
                        "title" : "Nick Michael's Fine Gallery",
                        "categories": categories,
                        "photos": photos}

        self.response.write(template.render(templateVars))

class CategoryArtPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicCategoryArt.html')

        categoryName =  self.request.get('categoryName')
        category = Category.query(Category.categoryName==categoryName).get()
        categoryKey = category.key

        photos = {}
        art = ArtPiece.query(ArtPiece.categories.IN([categoryKey]))

        for artpiece in art:
            photos[artpiece.key] = artpiece.picture.get()

        templateVars = {
                        "title" : category.categoryName,
                        "category": category,
                        "art": art,
                        "photos": photos}

        self.response.write(template.render(templateVars))


class ArtistsPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicArtists.html')

        photos = {}
        artists = Artist.query().order(Artist.firstName, Artist.lastName)

        for artist in artists:
            photos[artist.key] = artist.picture.get()

        templateVars = {
                        "title" : "Nick Michael's Fine Gallery",
                        "artists": artists,
                        "photos": photos}

        self.response.write(template.render(templateVars))


class ArtistArtPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicArtistArt.html')

        artistID =  self.request.get('artistID')
        artist = Artist.get_by_id(int(artistID))
        artistKey = artist.key

        photos = {}
        art = ArtPiece.query(ArtPiece.artist==artistKey)

        for artpiece in art:
            photos[artpiece.key] = artpiece.picture.get()

        templateVars = {
                        "title" : artist.firstName + " " + artist.lastName,
                        "artist": artist,
                        "art": art,
                        "photos": photos}

        self.response.write(template.render(templateVars))


class ArtPiecePage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicArtPiece.html')

        itemNumber =  self.request.get('itemNumber')
        artpiece = ArtPiece.query(ArtPiece.itemNumber==itemNumber).get()
        photo = File.query(File.key==artpiece.picture).get()
        artist = Artist.query(Artist.key==artpiece.artist).get()

        #create a comma separated string of categories
        categories = ndb.get_multi(artpiece.categories)
        categoryNamesList = []
        for category in categories:
            categoryNamesList.append(str(category.categoryName))
        categoriesString = ",".join(categoryNamesList)

        templateVars = {
                        "title" : artpiece.name,
                        "artpiece": artpiece,
                        "artist": artist,
                        "photo": photo,
                        "categories": categoriesString}

        self.response.write(template.render(templateVars))