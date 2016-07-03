"""
The flask application package.
"""

from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
#app.config.from_object('config')

dbconn = 'postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp' 
app.config['SQLALCHEMY_DATABASE_URI'] = dbconn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.secret_key = 'many random bytes'

#import BluePrints

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = 'Successful login'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in #todo localization'

from MyWebsite.mod_rescue.controllers import mod_resc_alert
from MyWebsite.mod_auth.controllers import mod_auth

# Register Blueprints
app.register_blueprint(mod_resc_alert)
app.register_blueprint(mod_auth)

print(app.url_map)
#print(app.url_defaults)



import MyWebsite.views




