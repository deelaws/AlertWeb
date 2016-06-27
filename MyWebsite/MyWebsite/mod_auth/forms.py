from wtforms import Form, BooleanField, TextField, SelectField, DateTimeField, validators
from wtforms.fields.html5 import DateField, EmailField
from MyWebsite.mod_profile.constants import *

class LoginForm(Form):
    user_name = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = TextField('Password', [validators.Length(min=10, max=password_max_length)])

class SignupForm(Form):
    user_name = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = TextField('Password', [validators.Length(min=10, max=password_max_length)])

    # @@ TODO: add first and last name as well.
    #          maybe not needed when facebook login integration is done.