from flask_sqlalchemy import SQLAlchemy
from MyWebsite import db
from MyWebsite.models import Base
from MyWebsite.mod_rescue.adventure_type import AdventureType
from MyWebsite.mod_rescue.constants import *
from datetime import datetime


"""
Represents a new rescue alert
"""
class RescueAlert(Base):

    #__tablename = 'RescueAlert'

    adventure_name = db.Column(db.String(adventure_name_max_length), nullable=False)

    # Type of adventure being undertaken  ._member_names_, name='adventure_type'
    adventure_type = db.Column(db.Integer, unique=True, nullable=False)
    
    # adventure start time
    adventure_start_time = db.Column(db.DateTime, unique=True, nullable=True)

    # Adventure end time. at this time, the alert will be kicked off
    adventure_end_time = db.Column(db.DateTime, unique=True, nullable=True)
    
    # If alert is active then a notification will be delivered to rescuers if
    # adventurer doesn't deactivate the alert before adventure_end_time
    alert_active = db.Column(db.Boolean, unique=False, default=False)

    # TODO: Rescuers

    def __init__(self, name, type, time_start, time_end):
        self.adventure_type = type._value_
        self.adventure_name = name
        self.adventure_start_time = time_start
        self.adventure_end_time = time_end

    def __repr__(self):
        return '<AdventureType %r>' % self.adventure_type
