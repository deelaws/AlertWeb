from flask_sqlalchemy import SQLAlchemy
from AlertWeb import db
from werkzeug.security import generate_password_hash, check_password_hash
from AlertWeb.models import Base
from AlertWeb.mod_profile.constants import *

'''
User model
'''
class User(Base):
    __tablename__ = 'user'

    '''
    Email address will be the username
    '''
    email = db.Column(db.String(user_name_max_length), unique=True, nullable=False)

    '''
    Encrypted password for the user.    
    '''
    password = db.Column(db.String, nullable=False)

    authenticated = db.Column(db.Boolean, default=False)

    admin = db.Column(db.Boolean, default=False)

    first_name = db.Column(db.String(user_name_max_length),  nullable=True)
    last_name = db.Column(db.String(user_name_max_length),  nullable=True)

    test_account = db.Column(db.Boolean, default=False)

    # One to many relationship with RescueAlert
    #rescue_alerts = db.relationship('RescueAlert', backref="user", cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, username, password):
        """Constructor"""
        self.email = username
        self.set_password(password)

    def set_password(self, password):
        """Set's the password for the user.
           It generates a hash of the password using werkzeug
        """
        print("password is", password)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Check's whether the specified password is correct """
        print("checking password")
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.admin

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email
    