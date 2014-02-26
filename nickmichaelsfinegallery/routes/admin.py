import webapp2

from controllers.FileUploadsController import *

app = webapp2.WSGIApplication([

    # Admin Routes
    (r'/admin', MainPage),
    (r'/admin/file', FileUploadFormHandler),
    (r'/admin/file/generate_upload_url', GenerateUploadUrlHandler),
    (r'/admin/file/upload', FileUploadHandler),
    (r'/admin/file/delete', DeleteFiles),
    (r'/admin/file/([^/]+)?', FileInfoHandler),
    (r'/admin/file/([^/]+)?/download', FileDownloadHandler),
    (r'/admin/file/([^/]+)?/success', AjaxSuccessHandler)

], debug=True )