"""
The flask application package.
"""

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
#app.config.from_object('config')

dbconn = 'postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp' 
app.config['SQLALCHEMY_DATABASE_URI'] = dbconn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

#import BluePrints

db = SQLAlchemy(app)

from MyWebsite.mod_rescue.controllers import mod_resc_alert

# Register Blueprints
app.register_blueprint(mod_resc_alert)
print(app.url_map)
#print(app.url_defaults)



import MyWebsite.views




