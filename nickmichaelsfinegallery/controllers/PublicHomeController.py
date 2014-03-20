import webapp2
import jinja2
import os

from models.category import Category
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

        photos = {}
        categories = Category.query().order(Category.categoryName)

        for category in categories:
            photos[category.key] = category.picture.get()

        templateVars = {
                        "title" : "Nick Michael's Fine Gallery",
                        "loginURL" : loginURL,
                        "loginTitle":loginTitle,
                        "categories": categories,
                        "photos": photos}

        self.response.write(template.render(templateVars))
