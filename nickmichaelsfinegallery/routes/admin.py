import webapp2

from controllers.AdminArtController import *
from controllers.AdminArtistsController import *
from controllers.AdminCategoriesController import *
from controllers.FileUploadsController import *


app = webapp2.WSGIApplication([

    #Admin Art Management
    (r'/admin', ArtPage),
    (r'/admin/art/upload', UploadArt),
    (r'/admin/art/edit', EditArt),
    (r'/admin/art/delete', DeleteArt),
    (r'/admin/art/deleteAll', DeleteAllArt),
    (r'/admin/art/refresh', RefreshArtTable),

    #Admin Artist Management
    (r'/admin/artists', ArtistsPage),
    (r'/admin/artists/create', CreateArtist),
    (r'/admin/artists/edit', EditArtist),
    (r'/admin/artists/delete', DeleteArtist),
    (r'/admin/artists/refresh', RefreshArtistTable),

    #Admin Category Management
    (r'/admin/categories', CategoriesPage),
    (r'/admin/categories/create', CreateCategory),
    (r'/admin/categories/edit', EditCategory),
    (r'/admin/categories/delete', DeleteCategory),
    (r'/admin/categories/refresh', RefreshCategoriesTable),

    #Admin Photo Uploads
    (r'/admin/photos', FileUploadFormHandler),
    (r'/admin/photos/generate_upload_url', GenerateUploadUrlHandler),
    (r'/admin/photos/upload', FileUploadHandler),
    (r'/admin/photos/delete', DeleteFiles),
    (r'/admin/photos/([^/]+)?', FileInfoHandler),
    (r'/admin/photos/([^/]+)?/download', FileDownloadHandler),
    (r'/admin/photos/([^/]+)?/success', AjaxSuccessHandler)

], debug=True )