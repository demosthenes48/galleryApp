import webapp2
import jinja2
import os
import logging

from models.artpiece import ArtPiece
from models.artpiece import Artist
from models.category import Category
from models.file import File

from google.appengine.ext import ndb
from google.appengine.api import search

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
        artpieces = {}

        allArt = ArtPiece.query(ArtPiece.categories.IN([categoryKey]),ArtPiece.slaveArtFlag==False)
        artistKeys = set([])
        for artpiece in allArt:
            #save the photo for this artipiece for later use
            photos[artpiece.key] = artpiece.picture.get()
            artistKeys.add(artpiece.artist)

        #get the list of artists who have art in this category
        artists = Artist.query(Artist.key.IN(list(artistKeys))).order(Artist.firstName, Artist.lastName)

        #create and save a list of artpieces for each artist that match this category
        for artist in artists:
            artistArt = []
            for artpiece in allArt:
                if artpiece.artist==artist.key:
                    artistArt.append(artpiece)
            artistArt.sort(key=lambda x: x.name)
            artpieces[artist.key] = artistArt

        templateVars = {
                        "title" : category.categoryName,
                        "category": category,
                        "artists": artists,
                        "artpieces": artpieces,
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
        art = ArtPiece.query(ArtPiece.artist==artistKey,ArtPiece.slaveArtFlag==False).order(ArtPiece.name)

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

        #check for additional sizes if this is a master or a slave piece
        additionalPieces = []
        if artpiece.masterArtFlag:
            slavePieces=ArtPiece.query(ArtPiece.masterArtPiece==artpiece.key)
            for slavepiece in slavePieces:
                additionalPieces.append(slavepiece)
        if artpiece.slaveArtFlag:
            masterArtPiece = ArtPiece.query(ArtPiece.key==artpiece.masterArtPiece).get()
            otherSlavePieces=ArtPiece.query(ArtPiece.masterArtPiece==masterArtPiece.key,ArtPiece.key<>artpiece.key)
            additionalPieces.append(masterArtPiece)
            for slavepiece in otherSlavePieces:
                additionalPieces.append(slavepiece)

        #generate the appropriate html to link to these other pieces if they exist
        additionalSizes = ""
        if len(additionalPieces) > 0:
            additionalSizes += "<h5>Also Available in Other Sizes:</h5><ul>"
            for additionalPiece in additionalPieces:
                additionalSizes += "<a href=\"/artpiece?itemNumber=" + additionalPiece.itemNumber + "\"><li>" + additionalPiece.name + " (" + additionalPiece.priceDisplay + ")</li></a>"
            additionalSizes += "</ul>"

        templateVars = {
                        "title" : artpiece.name,
                        "additionalSizes": additionalSizes,
                        "artpiece": artpiece,
                        "artist": artist,
                        "photo": photo,
                        "categories": categoriesString}

        self.response.write(template.render(templateVars))


class AboutUsPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicAboutUs.html')

        templateVars = {
                        "title" : "About Us"
                       }

        self.response.write(template.render(templateVars))


class SearchResults(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicSearchResults.html')
        searchString =  self.request.get('searchString')

        matchingArt = []

        #search for Art that matches
        index = search.Index(name="ArtPiece_index")
        try:
            search_query = search.Query(
                query_string=searchString,
                options=search.QueryOptions(
                limit=100))
            results = index.search(search_query)
            # Iterate over the documents in the results
            for artpieceDocument in results:
                artpiece = ArtPiece.get_by_id(int(artpieceDocument.doc_id))
                matchingArt.append(artpiece)
        except search.Error:
            logging.exception('Search failed')


        #now generate the appropriate HTML for each result
        if len(matchingArt) > 0:
            matchingArtHTML = """<ul class="thumbnails">"""
            for artpiece in matchingArt:
                matchingArtHTML += "<a href=\"/artpiece?itemNumber=" + artpiece.itemNumber + """\">
                                        <li class="span3">
                                            <div class="thumbnail">
                                                <div class="thumbnailHolder"><img src=\"""" +  artpiece.picture.get().thumbnail + """\""></div>
                                                <div class="caption">
                                                    <div class="artpieceName"><h5>""" + artpiece.name + """</h5></div>
                                                    <p>""" + artpiece.priceDisplay + """</p>
                                                </div>
                                            </div>
                                        </li>
                                    </a>"""
            matchingArtHTML += "</ul>"

        else:
            matchingArtHTML="No matches found"


        templateVars = {
                        "title" : 'Search Results',
                        "matchingArt": matchingArtHTML,
                        "searchString": searchString
                       }

        self.response.write(template.render(templateVars))