from flask_sqlalchemy import SQLAlchemy
from MyWebsite import db
from MyWebsite.models import Base
from MyWebsite.mod_profile.constants import *


'''
Profile model
'''
class Userprofile(Base):

    __tablename__ = 'user'

    '''
    Email address will be the username
    '''
    email = db.Column(db.String(user_name_max_length), primary_key=True, nullable=False)

    '''
    Encrypted password for the user.    
    '''
    password = db.Column(db.String(30), nullable=False)

    '''
    Name
    '''
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)

    authenticated = db.Column(db.Boolean, default=False)
    nick_name = db.Column(db.String(15), nullable=True)

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
    