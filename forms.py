from wtforms import Form, StringField, validators


class PhoneForm(Form):
    phonenumber = StringField('phonenumber', [validators.Length(min=8, max=10)])