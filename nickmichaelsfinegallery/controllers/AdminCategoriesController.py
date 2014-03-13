import webapp2
import jinja2
import os
import cgi
import logging

from models.category import Category
from models.file import File

from google.appengine.ext import ndb
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))))

class BaseHandler(webapp2.RequestHandler):
  def render_template(self, file, template_args):
    template = JINJA_ENVIRONMENT.get_template(file)
    self.response.write(template.render(template_args))

class CategoriesPage(BaseHandler):
    def get(self):
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
                        "title" : "Manage Categories",
                        "loginURL" : loginURL,
                        "loginTitle": loginTitle,
                        "categories": categories,
                        "photos": photos
                        }

        self.render_template("/templates/adminCategories.html", templateVars)

class RefreshCategoriesTable(BaseHandler):
    def get(self):
        photos = {}
        categories = Category.query().order(Category.categoryName)

        for category in categories:
            photos[category.key] = category.picture.get()
        html = ""
        for category in categories:
            html+="""<tr>
                        <td>""" + category.categoryName + """</td>
                        <td>""" + photos[category.key].file_name + """</td>
                        <td>
                            <a data-toggle="modal"  href="#editCategoryModal" onclick="fillCategoryEditModalDefaults(""" + str(category.key.id()) + ", '" + category.categoryName + "', '" + photos[category.key].file_name + """');" class="btn btn-medium">
                                <span class="glyphicon icon-edit"></span>
                            </a>
                            <a data-toggle="modal" data-id=\"""" + str(category.key.id()) + """\" href="#deleteCategoryModal" class="open-deleteCategoryModal btn btn-medium">
                                <span class="glyphicon icon-remove"></span>
                            </a>
                        </td>
                    </tr>"""

        self.response.write(html)

class CreateCategory(BaseHandler):
    def post(self):
        categoryName = self.request.get('categoryName')
        photoName = self.request.get('photoName')

        #get the photo specified by the user
        photo = File.query(File.file_name==photoName).get()

        #check to see if a category with that name already exists
        existingCategory = Category.query(Category.categoryName==categoryName).get()

        if existingCategory:
            #if an category with that name already exists, then update the information with the form data
            existingCategory.categoryName=categoryName
            existingCategory.picture=photo.key
            existingCategory.uploaded_by=users.get_current_user()

            existingCategory.put()
            message = "Successfully updated category record: " + existingCategory.categoryName

        else:
            #add a new category entry if no category with that name already exists
            category = Category(categoryName=categoryName, picture=photo.key, uploaded_by=users.get_current_user())
            category.put()
            message = "Successfully created category record: " + category.categoryName

        self.response.write(message)


class EditCategory(BaseHandler):
    def post(self):
        categoryKeyString = self.request.get('editCategoryKey')
        categoryID = int(categoryKeyString)
        categoryName = self.request.get('editCategoryName')
        photoName = self.request.get('editCategoryPhotoName')

        #get the photo specified by the user
        photo = File.query(File.file_name==photoName).get()

        #get the category based on the key and update all fields
        category = Category.get_by_id(categoryID)

        category.categoryName=categoryName
        category.picture=photo.key
        category.uploaded_by=users.get_current_user()

        category.put()

        message = "Successfully updated category record: " + category.categoryName
        self.response.write(message)


class DeleteCategory(BaseHandler):
    def post(self):
        categoryKeyString = self.request.get('deleteCategoryKey')

        #generate message
        category = Category.get_by_id(int(categoryKeyString))
        message = "Successfully deleted category: " + category.categoryName

        #delete category
        categoryKey = category.key
        categoryKey.delete()

        self.response.write(message)
