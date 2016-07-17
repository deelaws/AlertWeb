from wtforms import Form, BooleanField, TextField, SelectField, DateTimeField, validators
from wtforms.fields.html5 import DateField
from AlertWeb.mod_rescue.adventure_type import AdventureType, adventure_type_tuples
from AlertWeb.mod_rescue.constants import *

class CreateRescueAlertForm(Form):
    adventure_name = TextField('Alert Name', [validators.Length(min=4, max=adventure_name_max_length)])
    adventure_type = SelectField('AdventureType',  [validators.DataRequired()], choices=adventure_type_tuples)
    #adventure_start_time = DateTimeField('StartTime', [validators.DataRequired()], widget=DatePickerWidget())
    #adventure_end_time = DateTimeField('End Time', [validators.DataRequired()], widget=DatePickerWidget())
    adventure_start_time = DateField('StartTime', [validators.DataRequired()])
    adventure_end_time = DateField('End Time', [validators.DataRequired()])