from flask_sqlalchemy import SQLAlchemy
from MyWebsite.models import Base
from MyWebsite import db

"""
Represents a new rescue alert
"""
class RescueAlert(Base):

    #__tablename = 'RescueAlert'

    adventure_type = db.Column(db.Integer, unique=True)
    # adventure start time
    adventure_start_time = db.Column(db.DateTime, unique=True, nullable=True)
    # Adventure end time. at this time, the alert will be kicked off
    adventure_end_time = db.Column(db.DateTime, unique=True, nullable=True)
    
    # If alert is active then a notification will be delivered to rescuers if
    # adventurer doesn't deactivate the alert before adventure_end_time
    alert_active = db.Column(db.Boolean, unique=False, default=False)

    # TODO: Rescuers


    def __init__(self, adventure_type):
        self.adventure_type = adventure_type

    def __repr__(self):
        return '<AdventureType %r>' % self.adventure_type
