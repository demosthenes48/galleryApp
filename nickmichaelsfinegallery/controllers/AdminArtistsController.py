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
            logging.error("name: %s" % artist.firstName)

        templateVars = {
                        "title" : "Manage Artists",
                        "loginURL" : loginURL,
                        "loginTitle": loginTitle,
                        "artists": artists,
                        "photos": photos
                        }

        self.render_template("/templates/adminArtists.html", templateVars)

class CreateArtist(BaseHandler):
    def post(self):
        firstName = self.request.get('firstName')
        lastName = self.request.get('lastName')
        biography = self.request.get('biography')
        photoName = self.request.get('photoName')

        #get the photo specified by the user
        qry = File.query(File.file_name==photoName)
        photo = qry.get()

        #check to see if a artist with that name already exists
        qry = Artist.query(Artist.firstName==firstName and Artist.lastName==lastName)
        existingArtist = qry.get()

        if existingArtist:
            #if an artist with that name already exists, then update the information with the form data
            existingArtist.biography=biography
            existingArtist.firstName=firstName
            existingArtist.lastName=lastName
            existingArtist.picture=photo.key
            existingArtist.uploaded_by=users.get_current_user()

            existingArtist.put()
        else:
            #add a new artist entry if no artist with that name already exists
            artist = Artist(biography=biography, firstName=firstName, lastName=lastName, picture=photo.key, uploaded_by=users.get_current_user())
            artist.put()

        #Create a message to give the user some feedback
        message = """
                    <div class=\"row-fluid\">
                        <div class=\"span12\">
                            <h3>Submission successful</h3>
                            <p></p>
                        </div>
                    </div>
                """
        self.response.write(message)


class DeleteArtists(BaseHandler):
    def get(self):
        artists = Artist.query()
        for artist in artists:
            key = artist.key
            key.delete()
