from wtforms_alchemy import ModelForm
from database.database import Admin

class AdminForm(ModelForm):
    class Meta:
        model = Admin