import webapp2
import jinja2
import logging
import os
import csv

from models.file import File
from models.artpiece import ArtPiece
from models.artist import Artist
from models.category import Category
import urllib

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.api import images


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class BaseHandler(webapp2.RequestHandler):
  def render_template(self, file, template_args):
    template = JINJA_ENVIRONMENT.get_template(file)
    self.response.write(template.render(template_args))

class MainPage(BaseHandler):
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
        templateVars = {
                        "title" : "Nick Michael's Fine Gallery",
                        "loginURL" : loginURL,
                        "loginTitle":loginTitle
                        }

        self.render_template("/templates/adminHome.html", templateVars)


#File Upload Handlers

class FileUploadFormHandler(BaseHandler):
  @util.login_required
  def get(self):
    photos = File.query().order(File.file_name)
    self.render_template("/templates/fileUpload.html", {
        "title": "Manage Photos",
        'form_url': blobstore.create_upload_url('/admin/photos/upload'),
        'logout_url': users.create_logout_url('/'),
        'photos' : photos
    })


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        for blob_info in self.get_uploads():
            if not users.get_current_user():
                #if they are not logged in then delete all the upload data and redirect them to login
                for blob in self.get_uploads():
                    blob.delete()
                self.redirect(users.create_login_url("/"))
                return

            #if uploading a csv file, update the datastore to match records in file
            if blob_info.content_type == "application/vnd.ms-excel":
                blobdata=blobstore.BlobReader(blob_info)
                reader = csv.DictReader(blobdata,dialect='excel')
                self.response.headers['Content-Type'] = 'text/plain'

                for row in reader:
                    artist = row["Artist"]
                    categories = row["Categories"]
                    name = row["Name of Piece"]
                    price = row["Price($)"]
                    itemNumber = row["Item Number"]
                    width = row["Width(in)"]
                    height = row["Height(in)"]
                    depth = row["Depth(in)"]
                    weight = row["Weight"]
                    width = row["Width(in)"]
                    description = row["Product Description"]
                    colors = row["Colors"]
                    mediums = row["Mediums"]
                    masterNum = row["Master Art Piece (Item Number)"]
                    pictureName = row ["Picture Name"]

                    #check if artpiece with this item number already exists
                    qry = ArtPiece.query(ArtPiece.itemNumber==itemNumber)
                    existingArtPiece = qry.get()

                    #if existingArtPiece:
                        #if an artpiece with that itemNumber is already stored then update the record with the new information


                #delete and skip to the next file, we don't save excel files nor do we perform photo related code
                blob_info.delete()
                continue

            #otherwise we assume it is a photo (since it only allows jpg, png, gif, and csv)
            else:
                #check to see if a photo with that name already exists
                qry = File.query(File.file_name==blob_info.filename.upper())
                existingPhoto = qry.get()

                if existingPhoto:
                    #if a file with that name is already stored then replace the blob with the new uploaded file
                    blobstore.delete(existingPhoto.blob)
                    existingPhoto.blob = blob_info.key()
                    existingPhoto.uploaded_by=users.get_current_user()
                    existingPhoto.url=images.get_serving_url(blob_info.key())

                    existingPhoto.put()
                else:
                    #add a new file entry if no file with that name already exists
                    file = File(blob=blob_info.key(), file_name=blob_info.filename.upper(), uploaded_by=users.get_current_user(), url=images.get_serving_url(blob_info.key()))
                    file.put()

                self.redirect("/admin/photos/%s/success" % blob_info.key())


class AjaxSuccessHandler(BaseHandler):
    def get(self, file_id):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('%s/file/%s' % (self.request.host_url, file_id))


class FileInfoHandler(BaseHandler):
  def get(self, file_id):
    file_info = blobstore.BlobInfo.get(file_id)
    if not file_info:
        self.error(404)
        return

    img = images.Image(blob_key=file_id)

    self.response.headers['Content-Type'] = 'image/jpeg'
    self.response.out.write(img)

    #logging.error("%s" % images.get_serving_url(file_id, size=None, crop=False, secure_url=None))
    #self.redirect(images.get_serving_url(file_id, size=None, crop=False, secure_url=None))


class FileDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, file_id):
    file_id = str(urllib.unquote(file_id))
    file_info = blobstore.BlobInfo.get(file_id)
    if not file_info:
      self.error(404)
      return
    self.send_blob(file_info, save_as=True)


class GenerateUploadUrlHandler(BaseHandler):
  @util.login_required
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(blobstore.create_upload_url('/admin/photos/upload'))


class RefreshPhotoThumbnails(BaseHandler):
    def get(self):

        #sort the art by artist name and then by artpiece name
        photos = File.query().order(File.file_name)

        html = ""
        for photo in photos:
            html+="""<li class="span3">
                        <div class="thumbnail">
                            <img data-src="holder.js/300x200" alt="300x200" style="width: 300px; height: 200px;" src=""" + photo.url + """>
                            <div class="caption">
                                <div class="artpieceName">
                                    <h5>""" + photo.file_name + """</h5>
                                    <a data-toggle="modal"  href="#editPhotoModal" onclick="fillEditPhotoModalDefaults(""" + str(photo.key.id()) + """,'""" + photo.file_name + """');" class="btn btn-medium">
                                        <span class="glyphicon icon-edit"></span>
                                    </a>
                                    <a data-toggle="modal" data-id=""" + str(photo.key.id()) + """ href="#deletePhotoModal" class="open-deletePhotoModal btn btn-medium">
                                        <span class="glyphicon icon-remove"></span>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </li>"""

        self.response.write(html)


class EditFile(BaseHandler):
    def post(self):
        fileKeyString = self.request.get('editPhotoKey')
        newPhotoName = self.request.get('editPhotoName').upper()
        fileToEdit = File.get_by_id(int(fileKeyString))

        #check if another file with that name already exists
        oldFile= File.query(File.file_name==newPhotoName).get()
        if oldFile:
            message = "ERROR: A file with that name already exists"
        else:
            #Find and update the file name of the current file(not possible to do on the actual blob)
            fileToEdit.file_name = newPhotoName
            fileToEdit.put()
            message = "Successfully updated photo name: " + fileToEdit.file_name

        self.response.write(message)


class DeleteFile(BaseHandler):
    def post(self):
        fileKeyString = self.request.get('deletePhotoKey')

        #generate message
        file = File.get_by_id(int(fileKeyString))
        message = "Successfully deleted photo: " + file.file_name

        #delete file
        blobstore.delete(file.blob)
        key = file.key
        key.delete()

        self.response.write(message)


class DeleteAllFiles(BaseHandler):
    def get(self):
        files = File.query()
        for file in files:
            blobstore.delete(file.blob)
            key = file.key
            key.delete()

