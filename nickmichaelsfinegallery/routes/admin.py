import webapp2

from controllers.FileUploadsController import *

app = webapp2.WSGIApplication([

    # Admin Routes
    (r'/admin', MainPage),
    (r'/admin/photos', FileUploadFormHandler),
    (r'/admin/photos/generate_upload_url', GenerateUploadUrlHandler),
    (r'/admin/photos/upload', FileUploadHandler),
    (r'/admin/photos/delete', DeleteFiles),
    (r'/admin/photos/([^/]+)?', FileInfoHandler),
    (r'/admin/photos/([^/]+)?/download', FileDownloadHandler),
    (r'/admin/photos/([^/]+)?/success', AjaxSuccessHandler)

], debug=True )