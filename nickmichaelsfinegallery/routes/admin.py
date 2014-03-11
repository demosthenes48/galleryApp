import webapp2

from controllers.FileUploadsController import *
from controllers.AdminArtistsController import *

app = webapp2.WSGIApplication([

    # Admin Page RoutesRoutes
    (r'/admin', MainPage),
    (r'/admin/photos', FileUploadFormHandler),

    #Admin Artist Management
    (r'/admin/artists', ArtistsPage),
    (r'/admin/artists/create', CreateArtist),
    (r'/admin/artists/edit', EditArtist),
    (r'/admin/artists/delete', DeleteArtist),

    #Admin Photo Uploads
    (r'/admin/photos/generate_upload_url', GenerateUploadUrlHandler),
    (r'/admin/photos/upload', FileUploadHandler),
    (r'/admin/photos/delete', DeleteFiles),
    (r'/admin/photos/([^/]+)?', FileInfoHandler),
    (r'/admin/photos/([^/]+)?/download', FileDownloadHandler),
    (r'/admin/photos/([^/]+)?/success', AjaxSuccessHandler)

], debug=True )