import webapp2

from controllers.PublicHomeController import *

app = webapp2.WSGIApplication([

    # Public Routes
    (r'/', MainPage),
    (r'/category', CategoryArtPage),
    (r'/artists', ArtistsPage),
    (r'/artist', ArtistArtPage),
    (r'/artpiece', ArtPiecePage)


], debug=True )