"""
The flask application package.
"""

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

dbconn = 'postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp' 
app.config['SQLALCHEMY_DATABASE_URI'] = dbconn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


import MyWebsite.views

#import BluePrints

