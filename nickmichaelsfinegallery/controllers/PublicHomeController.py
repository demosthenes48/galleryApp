import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/PublicHome.html')
        templateVars = { "title" : "Nick Michael's Fine Gallery"}
        self.response.write(template.render(templateVars))
