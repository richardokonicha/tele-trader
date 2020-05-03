from wtforms.ext.sqlalchemy.orm import model_form
from database import Admin
AdminForm = model_form(Admin)