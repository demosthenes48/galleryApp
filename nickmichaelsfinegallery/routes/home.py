import webapp2

from controllers.baseController import *

app = webapp2.WSGIApplication([

    # Public Routes
    (r'/', MainPage),
    (r'/file', FileUploadFormHandler),
    (r'/file/upload', FileUploadHandler),
    (r'/file/([^/]+)?', FileInfoHandler),
    (r'/file/([^/]+)?/download', FileDownloadHandler),
    (r'/file/([^/]+)?/success', AjaxSuccessHandler)

], debug=True )