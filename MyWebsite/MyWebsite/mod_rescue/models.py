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

    adventure_name = db.Column(db.String(adventure_name_max_length), nullable=False)

    # Type of adventure being undertaken.
    # Could have used ENUM type in database but this is more simple.
    # We can locally maintain an easy mapping of int to string in the app.
    adventure_type = db.Column(db.Integer, unique=False, nullable=False)

    '''
    NOTE: All times are stored in UTC time.
    '''
    # adventure start time 
    adventure_start_time = db.Column(db.DateTime, unique=False, nullable=True)

    # Adventure end time. at this time, the alert will be kicked off
    adventure_end_time = db.Column(db.DateTime, unique=False, nullable=True)
    
    # If alert is active then a notification will be delivered to rescuers if
    # adventurer doesn't deactivate the alert before adventure_end_time
    alert_active = db.Column(db.Boolean, unique=False, default=False)

    # Each Rescue is associate with a USER.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref="rescue_alerts")

    '''
    If public then, anyone can view the rescue alert
    '''
    # is_public = db.Column(db.Boolean, default=False)

    # TODO: Rescuers

    def __init__(self, name, type, time_start, time_end):
        self.adventure_type = type
        self.adventure_name = name
        self.adventure_start_time = time_start
        self.adventure_end_time = time_end
        self.alert_active = False

    def activate_alert(self):
        if  self.adventure_start_time == None or \
            self.adventure_end_time   == None:
            return False
        self.alert_active = True
        return True
    
    def deactivate_alert(self):
        self.alert_active = False

    def send_alert(self):
        print("sending alert for adventure {}".format(self))

    def __repr__(self):
        return 'Alert: name=%s endtime=%s AdventureType %r' % (self.adventure_name,
                                                                self.adventure_end_time,
                                                                self.adventure_type)
