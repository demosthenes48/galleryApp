import webapp2
import jinja2
import os
import cgi
import logging

from models.artist import Artist
from models.file import File

from google.appengine.ext import ndb
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class BaseHandler(webapp2.RequestHandler):
  def render_template(self, file, template_args):
    template = JINJA_ENVIRONMENT.get_template(file)
    self.response.write(template.render(template_args))

class ArtistsPage(BaseHandler):
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

        photos = {}
        artists = Artist.query().order(Artist.firstName, Artist.lastName)

        for artist in artists:
            photos[artist.key] = artist.picture.get()

        templateVars = {
                        "title" : "Manage Artists",
                        "loginURL" : loginURL,
                        "loginTitle": loginTitle,
                        "artists": artists,
                        "photos": photos
                        }

        self.render_template("/templates/adminArtists.html", templateVars)

class RefreshArtistTable(BaseHandler):
    def get(self):
        photos = {}
        artists = Artist.query().order(Artist.firstName, Artist.lastName)

        for artist in artists:
            photos[artist.key] = artist.picture.get()
        html = ""
        for artist in artists:
            html+="""<tr>
                        <td>""" + artist.firstName + """</td>
                        <td>""" + artist.lastName + """</td>
                        <td>""" + artist.biography + """</td>
                        <td>""" + photos[artist.key].file_name + """</td>
                        <td>
                            <a data-toggle="modal"  href="#editArtistModal" onclick="fillEditModalDefaults(""" + str(artist.key.id()) + ", '" + artist.firstName +"', '" + artist.lastName +"', '" + artist.biography + "', '" + photos[artist.key].file_name + """');" class="btn btn-medium">
                                <span class="glyphicon icon-edit"></span>
                            </a>
                            <a data-toggle="modal" data-id=\"""" + str(artist.key.id()) + """\" href="#deleteArtistModal" class="open-deleteArtistModal btn btn-medium">
                                <span class="glyphicon icon-remove"></span>
                            </a>
                        </td>
                    </tr>"""

        self.response.write(html)

class CreateArtist(BaseHandler):
    def post(self):
        firstName = self.request.get('firstName')
        lastName = self.request.get('lastName')
        biography = self.request.get('biography')
        photoName = self.request.get('photoName')

        #get the photo specified by the user
        photo = File.query(File.file_name==photoName.upper()).get()

        #check to see if a artist with that name already exists
        existingArtist = Artist.query(Artist.firstName==firstName and Artist.lastName==lastName).get()

        if existingArtist:
            #if an artist with that name already exists, then update the information with the form data
            existingArtist.biography=biography
            existingArtist.firstName=firstName
            existingArtist.lastName=lastName
            existingArtist.picture=photo.key
            existingArtist.uploaded_by=users.get_current_user()

            existingArtist.put()
            existingArtist.add_to_search_index()
            message = "Successfully updated artist record: " + existingArtist.firstName + " " + existingArtist.lastName

        else:
            #add a new artist entry if no artist with that name already exists
            artist = Artist(biography=biography, firstName=firstName, lastName=lastName, picture=photo.key, uploaded_by=users.get_current_user())
            artist.put()
            artist.add_to_search_index()
            message = "Successfully created artist record: " + artist.firstName + " " + artist.lastName

        self.response.write(message)


class EditArtist(BaseHandler):
    def post(self):
        artistKeyString = self.request.get('editArtistKey')
        artistID = int(artistKeyString)
        firstName = self.request.get('editFirstName')
        lastName = self.request.get('editLastName')
        biography = self.request.get('editBiography')
        photoName = self.request.get('editPhotoName')

        #get the photo specified by the user
        photo = File.query(File.file_name==photoName.upper()).get()

        #get the artist based on the key and update all fields
        artist = Artist.get_by_id(artistID)

        artist.biography=biography
        artist.firstName=firstName
        artist.lastName=lastName
        artist.picture=photo.key
        artist.uploaded_by=users.get_current_user()

        artist.put()
        artist.add_to_search_index()

        message = "Successfully updated artist record: " + artist.firstName + " " + artist.lastName
        self.response.write(message)


class DeleteArtist(BaseHandler):
    def post(self):
        artistKeyString = self.request.get('deleteArtistKey')

        #generate message
        artist = Artist.get_by_id(int(artistKeyString))
        artist.remove_from_search_index()
        message = "Successfully deleted artist: " + artist.firstName + " " + artist.lastName

        #delete artist
        artistKey = artist.key
        artistKey.delete()

        self.response.write(message)


class DeleteAllArtistIndexes(BaseHandler):
    def get(self):
        artists=Artist.query()
        for artist in artists:
            artist.remove_from_search_index()
            logging.error("removed index for: %s" % artist.firstName)
