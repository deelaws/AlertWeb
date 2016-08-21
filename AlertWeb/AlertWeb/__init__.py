"""
The flask application package.
"""
import os
from flask import Flask, g, session
from flask_login import LoginManager
from flask_mail import Mail, Message

from flask_sqlalchemy import SQLAlchemy
from AlertWeb.config import configuration


mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_message = 'Successful login'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in #todo localization'

def create_app(config_name):
    app = Flask(__name__)

    # Initialize app form the specified config name
    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from AlertWeb.mod_rescue.controllers import mod_resc_alert
    from AlertWeb.mod_auth.controllers import mod_auth
    from AlertWeb.mod_main import mod_main

    # Register Blueprints
    app.register_blueprint(mod_resc_alert)
    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_main)

    print(app.url_map)

    @app.before_request
    def add_user_to_g():
        from AlertWeb.mod_auth.models import User
        if session.get("user_id"):
            user_obj = User.query.filter_by(email=session["user_id"]).first()
        else:
            user_obj = None #{"name": "Guest"}  # Make it better, use an anonymous User instead
        g.user = user_obj
    
    return app
