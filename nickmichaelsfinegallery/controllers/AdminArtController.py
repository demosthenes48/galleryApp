import webapp2
import jinja2
import os
import csv
import logging

from models.artpiece import ArtPiece
from models.artist import Artist
from models.category import Category
from models.file import File

from decimal import Decimal
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import util


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class BaseHandler(webapp2.RequestHandler):
  def render_template(self, file, template_args):
    template = JINJA_ENVIRONMENT.get_template(file)
    self.response.write(template.render(template_args))


class ArtPage(BaseHandler):
    def get(self):
        loginTitle = ""
        loginURL = ""
        user = users.get_current_user()
        if user:
            loginTitle = "logout"
            loginURL= users.create_logout_url('/')
        else:
            loginTitle = "login"
            loginURL= users.create_login_url('/')

        uploadURL = blobstore.create_upload_url('/admin/art/upload')
        categoriesList = {}
        masterItemNumberList = {}
        art = []

        #sort the art by artist name and then by artpiece name
        artists = Artist.query().order(Artist.firstName, Artist.lastName)
        for artist in artists:
            artistArt = ArtPiece.query().order(ArtPiece.name).filter(ArtPiece.artist==artist.key)
            for artpiece in artistArt:
                art.append(artpiece)

        for artpiece in art:
            #create a comma separated string of categories
            categories = ndb.get_multi(artpiece.categories)
            categoryNamesList = []
            for category in categories:
                categoryNamesList.append(str(category.categoryName))
            categoryNamesString = ",".join(categoryNamesList)
            categoriesList[artpiece.key] = categoryNamesString

            #check for null master art piece
            itemNumber = '' if artpiece.masterArtPiece is None else artpiece.masterArtPiece.get().itemNumber
            masterItemNumberList[artpiece.key] = itemNumber


        templateVars = {
                        "title" : "Manage Art",
                        "loginURL" : loginURL,
                        "loginTitle": loginTitle,
                        "art": art,
                        "categoriesList": categoriesList,
                        "masterItemNumberList": masterItemNumberList,
                        "uploadURL": uploadURL
                        }

        self.render_template("/templates/adminArt.html", templateVars)


class RefreshArtTable(BaseHandler):
    def get(self):
        categoriesList = {}
        art = []

        #sort the art by artist name and then by artpiece name
        artists = Artist.query().order(Artist.firstName, Artist.lastName)
        for artist in artists:
            artistArt = ArtPiece.query().order(ArtPiece.name).filter(ArtPiece.artist==artist.key)
            for artpiece in artistArt:
                art.append(artpiece)

        for artpiece in art:
            categories = ndb.get_multi(artpiece.categories)
            categoryNamesList = []
            for category in categories:
                categoryNamesList.append(str(category.categoryName))
            categoryNamesString = ",".join(categoryNamesList)
            categoriesList[artpiece.key] = categoryNamesString
        html = ""
        for artpiece in art:
            html+="""<tr>
                        <td>""" + artpiece.artist.get().firstName  + " " +  artpiece.artist.get().lastName + """</td>
                        <td>""" + artpiece.name + """</td>
                        <td>""" + artpiece.itemNumber + """</td>
                        <td>""" + categoriesList[artpiece.key] + """</td>
                        <td>""" + artpiece.priceDisplay + """</td>
                        <td>
                            <a data-toggle="modal"  href="#editArtModal" onclick="fillEditArtModalDefaults(""" + str(artpiece.key.id()) + ",'" + artpiece.artist.get().firstName + " " + artpiece.artist.get().lastName + "', '" + categoriesList[artpiece.key] + "', '" + artpiece.name + "', '" + artpiece.price + "', '" + artpiece.itemNumber + "', '" + artpiece.width + "', '" + artpiece.height + "', '" + artpiece.depth + "', '" + artpiece.weight + "', '" + artpiece.description + "', '" + artpiece.colors + "', '" + artpiece.mediums + "', '" + ('' if artpiece.masterArtPiece is None else artpiece.masterArtPiece.get().itemNumber) + "', '" + artpiece.picture.get().file_name + """');" class="btn btn-medium">
                                <span class="glyphicon icon-edit"></span>
                            </a>
                            <a data-toggle="modal" data-id=\"""" + str(artpiece.key.id()) + """\" href="#deleteArtModal" class="open-deleteArtModal btn btn-medium">
                                <span class="glyphicon icon-remove"></span>
                            </a>
                        </td>
                    </tr>"""

        self.response.write(html)

class UploadArt(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        blob_info = self.get_uploads()[0]

        #only act on the file if it is a .csv, .xls, or .xlsx file type
        if blob_info.content_type == "application/vnd.ms-excel" or blob_info.content_type == ".csv" or blob_info.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            blobdata=blobstore.BlobReader(blob_info)
            reader = csv.DictReader(blobdata,dialect='excel')
            self.response.headers['Content-Type'] = 'text/plain'
            message = ""
            editedMessage = ""
            createdMessage = ""

            for row in reader:
                artistString = row["Artist"]
                categoriesString = row["Categories"]
                name = row["Name of Piece"]
                price = row["Price($)"]
                priceDisplay = "$" + '{:20,.2f}'.format(Decimal(price))
                itemNumber = row["Item Number"]
                height = row["Height(in)"]
                depth = row["Depth(in)"]
                weight = row["Weight"]
                width = row["Width(in)"]
                description = row["Product Description"]
                colors = row["Colors"]
                mediums = row["Mediums"]
                masterItemNum = row["Master Art Piece (Item Number)"]
                pictureName = row ["Picture Name"]

                #find related objects to tie to this artpiece
                artistNameList=artistString.split(" ")
                artistFirstName=artistNameList[0]
                artistLastName=artistNameList[-1]
                artist = Artist.query(Artist.firstName==artistFirstName, Artist.lastName==artistLastName).get()
                categories = []
                categoriesList = categoriesString.split(",")
                for categoryString in categoriesList:
                    category = Category.query(Category.categoryName==categoryString.strip()).get()
                    categories.append(category)
                masterArtPiece = ArtPiece.query(ArtPiece.itemNumber==masterItemNum).get()
                photo = File.query(File.file_name==pictureName.upper()).get()

                #check if artpiece with this item number already exists
                existingArtPiece = ArtPiece.query(ArtPiece.itemNumber==itemNumber).get()

                if existingArtPiece:
                    #if an artpiece with that itemNumber is already stored then update the record with the new information
                    existingArtPiece.artist = artist.key
                    existingArtPiece.categories = []
                    for category in categories:
                        existingArtPiece.categories.append(category.key)
                    existingArtPiece.colors = colors
                    existingArtPiece.depth = depth
                    existingArtPiece.description = description
                    existingArtPiece.height = height
                    if masterArtPiece:
                        existingArtPiece.masterArtPiece = masterArtPiece.key
                    existingArtPiece.mediums = mediums
                    existingArtPiece.name = name
                    existingArtPiece.picture = photo.key
                    existingArtPiece.price = price
                    existingArtPiece.priceDisplay = priceDisplay
                    existingArtPiece.uploaded_by=users.get_current_user()
                    existingArtPiece.weight = weight
                    existingArtPiece.width = width

                    existingArtPiece.put()

                    editedMessage += "<br>" + existingArtPiece.name

                else:
                    #otherwise create a new record for the artpiece
                    artPiece = ArtPiece(artist=artist.key, colors=colors, depth=depth, description=description, height=height, itemNumber=itemNumber, mediums=mediums, name=name, picture=photo.key, price=price, priceDisplay=priceDisplay, weight=weight, width=width, uploaded_by=users.get_current_user())
                    for category in categories:
                        artPiece.categories.append(category.key)
                    if masterArtPiece:
                        artPiece.masterArtPiece = masterArtPiece.key

                    artPiece.put()

                    createdMessage += "<br>" + artPiece.name

            #no need to save the file in the blobstore
            blob_info.delete()

            message = "The following items were added to the database: <br>"
            message += createdMessage + "<br><br>"
            message+= "The following items were updated in the database: <br>"
            message += editedMessage

            self.response.write(message)


class EditArt(BaseHandler):
    def post(self):
        artpieceKeyString = self.request.get('editArtKey')
        artpieceID = int(artpieceKeyString)
        artistString = self.request.get('editArtist')
        categoriesString = self.request.get('editCategories')
        name = self.request.get('editName')
        price = self.request.get('editPrice')
        priceDisplay = "$" + '{:20,.2f}'.format(Decimal(price))
        itemNumber = self.request.get('editItemNumber')
        width = self.request.get('editWidth')
        height = self.request.get('editHeight')
        depth = self.request.get('editDepth')
        weight = self.request.get('editWeight')
        description = self.request.get('editProductDescription')
        colors = self.request.get('editColors')
        mediums = self.request.get('editMediums')
        masterItemNum = self.request.get('editMasterArtNum')
        pictureName = self.request.get('editProductPhotoName')

        #find related objects to tie to this artpiece
        artistNameList=artistString.split(" ")
        artistFirstName=artistNameList[0]
        artistLastName=artistNameList[-1]
        artist = Artist.query(Artist.firstName==artistFirstName, Artist.lastName==artistLastName).get()
        categories = []
        categoriesList = categoriesString.split(",")
        for categoryString in categoriesList:
            category = Category.query(Category.categoryName==categoryString.strip()).get()
            categories.append(category)
        masterArtPiece = ArtPiece.query(ArtPiece.itemNumber==masterItemNum).get()
        photo = File.query(File.file_name==pictureName.upper()).get()

        #get the artpiece based on the key and update all fields accordingly
        artpiece = ArtPiece.get_by_id(artpieceID)

        artpiece.artist = artist.key
        artpiece.categories = []
        for category in categories:
            artpiece.categories.append(category.key)
        artpiece.colors = colors
        artpiece.depth = depth
        artpiece.description = description
        artpiece.height = height
        artpiece.itemNumber = itemNumber
        if masterArtPiece:
            artpiece.masterArtPiece = masterArtPiece.key
        artpiece.mediums = mediums
        artpiece.name = name
        artpiece.picture = photo.key
        artpiece.price = price
        artpiece.priceDisplay = priceDisplay
        artpiece.uploaded_by=users.get_current_user()
        artpiece.weight = weight
        artpiece.width = width

        artpiece.put()

        message = "Successfully updated artpiece record: " + artpiece.name
        self.response.write(message)


class DeleteArt(BaseHandler):
    def post(self):
        artKeyString = self.request.get('deleteArtKey')

        #generate message
        artpiece = ArtPiece.get_by_id(int(artKeyString))
        message = "Successfully deleted artpiece: " + artpiece.name

        #delete category
        artpieceKey = artpiece.key
        artpieceKey.delete()

        self.response.write(message)

class DeleteAllArt(BaseHandler):
    def get(self):
        allArt = ArtPiece.query()
        for art in allArt:
            artKey = art.key
            artKey.delete()
