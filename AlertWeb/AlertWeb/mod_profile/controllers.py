from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from AlertWeb import db, login_manager
from AlertWeb.mod_rescue.forms import CreateRescueAlertForm
from AlertWeb.mod_profile.models import Userprofile
from flask_login import LoginManager

'''
The @login_manager.user_loader piece tells Flask-login how to load users 
given an id.
'''
@login_manager.user_loader
def load_user(user_id):
    return Userprofile.query.get(user_id)