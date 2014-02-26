import webapp2

from controllers.PublicHomeController import *

app = webapp2.WSGIApplication([

    # Public Routes
    (r'/', MainPage)

], debug=True )