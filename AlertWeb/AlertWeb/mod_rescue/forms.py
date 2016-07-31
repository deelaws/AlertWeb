from wtforms import Form, BooleanField, TextField, SelectField, validators,ValidationError
from wtforms.fields.html5 import DateField, DateTimeField
from AlertWeb.mod_rescue.adventure_type import AdventureType, adventure_type_tuples
from AlertWeb.mod_rescue.constants import *
from datetime import datetime

def convert_client_time(time):
    print(time)
    return datetime.strptime(time, '%m/%d/%Y %I:%M %p')

def adventure_start_time_validator(form, field):
    print(field.raw_data)
    conv_time = convert_client_time(field.raw_data[0])
    # time must be greater than now.
    if conv_time < datetime.now():
        raise ValidationError("Start time must be in the future")

def adventure_end_time_validator(form, field):
    if form.adventure_start_time:
        start_time = convert_client_time(form.adventure_start_time.raw_data[0])
        end_time = convert_client_time(field.raw_data[0])
        # time must be greater than now.
        if end_time < start_time:
            raise ValidationError("End time must be after start time")
    else:
        raise ValidationError("Enter the start date and time first")

class CreateRescueAlertForm(Form):
    adventure_name = TextField('Alert Name', [validators.Length(min=4, max=adventure_name_max_length)])
    adventure_type = SelectField('AdventureType', [validators.DataRequired()], coerce=int, choices=adventure_type_tuples)

    adventure_start_time = TextField('Start Time and Date', [validators.DataRequired(), adventure_start_time_validator])
    adventure_end_time = TextField('End Time and Date', [validators.DataRequired(), adventure_end_time_validator])
    