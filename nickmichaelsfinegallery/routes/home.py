import webapp2

from controllers.BaseController import *

app = webapp2.WSGIApplication([

    # Public Routes
    (r'/', MainPage)

], debug=True )