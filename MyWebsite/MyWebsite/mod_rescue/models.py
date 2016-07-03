from flask_sqlalchemy import SQLAlchemy
from MyWebsite import db
from MyWebsite.models import Base
from MyWebsite.mod_rescue.adventure_type import AdventureType
from MyWebsite.mod_rescue.constants import *
from MyWebsite.mod_profile.constants import *
from datetime import datetime
from MyWebsite.mod_auth.models import User

"""
Represents a new rescue alert
"""
class RescueAlert(Base):

    __tablename__ = 'rescue_alert'

    id            = db.Column(db.Integer,   primary_key=True)

    adventure_name = db.Column(db.String(adventure_name_max_length), nullable=False)

    # Type of adventure being undertaken  ._member_names_, name='adventure_type'
    adventure_type = db.Column(db.Integer, unique=False, nullable=False)
    
    # adventure start time
    adventure_start_time = db.Column(db.DateTime, unique=False, nullable=True)

    # Adventure end time. at this time, the alert will be kicked off
    adventure_end_time = db.Column(db.DateTime, unique=False, nullable=True)
    
    # If alert is active then a notification will be delivered to rescuers if
    # adventurer doesn't deactivate the alert before adventure_end_time
    alert_active = db.Column(db.Boolean, unique=False, default=False)

    # Each Rescue is associate with a USER.
    user_email = db.Column(db.String(user_name_max_length), db.ForeignKey('user.email'))

    '''
    If public then, anyone can view the rescue alert
    '''
    # admin = db.Column(db.Boolean, default=False)

    # TODO: Rescuers

    def __init__(self, name, type, time_start, time_end):
        self.adventure_type = type._value_
        self.adventure_name = name
        self.adventure_start_time = time_start
        self.adventure_end_time = time_end

    def __repr__(self):
        return '<AdventureType %r>' % self.adventure_type
