import webapp2
import jinja2
import logging
import os
from models.file import File
import urllib

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util


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
                        "loginTitle":loginTitle}

        self.render_template("/templates/base.html", templateVars)


#Photo Upload Handlers

class FileUploadFormHandler(BaseHandler):
  @util.login_required
  def get(self):
    self.render_template("/templates/fileUpload.html", {
        'form_url': blobstore.create_upload_url('/file/upload'),
        'logout_url': users.create_logout_url('/'),
    })


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        for blob_info in self.get_uploads():
            if not users.get_current_user():
                blob_info.delete()
                self.redirect(users.create_login_url("/"))
                return

            file = File(blob=blob_info.key(), file_name=blob_info.filename, uploaded_by=users.get_current_user())
            file.put()

            self.redirect("/file/%s/success" % blob_info.key())


class AjaxSuccessHandler(BaseHandler):
    def get(self, file_id):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('%s/%s' % (self.request.host_url, file_id))


class FileInfoHandler(BaseHandler):
  def get(self, file_id):
    file_id = str(urllib.unquote(file_id))
    file_info = blobstore.BlobInfo.get(file_id)
    if not file_info:
      self.error(404)
      return
    self.render_template("/templates/fileInfo.html", {
        'file_info': file_info,
        'logout_url': users.create_logout_url('/'),
    })


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
    self.response.out.write(blobstore.create_upload_url('/file/upload'))