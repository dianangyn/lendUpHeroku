from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class webFizzForm(Form):
    phonenumber = StringField('openid', validators=[DataRequired()])
