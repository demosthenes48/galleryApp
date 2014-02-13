import webapp2

from controllers.BaseController import *

app = webapp2.WSGIApplication([

    # Public Routes
    (r'/', MainPage),
    (r'/file', FileUploadFormHandler),
    (r'/file/generate_upload_url', GenerateUploadUrlHandler),
    (r'/file/upload', FileUploadHandler),
    (r'/file/([^/]+)?', FileInfoHandler),
    (r'/file/([^/]+)?/download', FileDownloadHandler),
    (r'/file/([^/]+)?/success', AjaxSuccessHandler)

], debug=True )