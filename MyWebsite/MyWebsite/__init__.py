"""
The flask application package.
"""

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from MyWebsite.adventure_type import AdventureType

app = Flask(__name__)

dbconn = 'postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp' 
app.config['SQLALCHEMY_DATABASE_URI'] = dbconn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

"""
Represents a new rescue alert
"""
class RescueAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adventure_type = db.Column(db.Integer, unique=True)
    # adventure start time
    start_time = db.Column(db.DateTime, unique=True)
    # Adventure end time. at this time, the alert will be kicked off
    end_time = db.Column(db.DateTime, unique=True)


    def __init__(self, adventure_type):
        self.adventure_type = adventure_type

    def __repr__(self):
        return '<AdventureType %r>' % self.adventure_type

import MyWebsite.views



