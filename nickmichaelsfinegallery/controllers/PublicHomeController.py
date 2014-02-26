import webapp2
import jinja2
import os

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/publicHome.html')


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

        self.response.write(template.render(templateVars))
