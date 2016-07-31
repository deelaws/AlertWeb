from wtforms import Form, BooleanField, TextField, SelectField, validators
from wtforms.fields.html5 import DateField, DateTimeField
from AlertWeb.mod_rescue.adventure_type import AdventureType, adventure_type_tuples
from AlertWeb.mod_rescue.constants import *

class CreateRescueAlertForm(Form):
    adventure_name = TextField('Alert Name', [validators.Length(min=4, max=adventure_name_max_length)])
    adventure_type = SelectField('AdventureType', [validators.DataRequired()], coerce=int, choices=adventure_type_tuples)

    adventure_end_date = DateField('Finish Date')

    adventure_start_time = DateTimeField('Start Time')