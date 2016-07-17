"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, g, session
from AlertWeb import app
from flask_login import login_required
from AlertWeb.mod_auth.models import User

@app.before_request
def add_user_to_g():
    if session.get("user_id"):
        user_obj = User.query.filter_by(email=session["user_id"]).first()
    else:
        user_obj = None #{"name": "Guest"}  # Make it better, use an anonymous User instead
    g.user = user_obj

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    print("home function*******")
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
    
@app.route('/contact')
def contact():
    """Renders the contact page."""
    ab = 1
    print(ab)
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
@login_required
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/profile')
@login_required
def profile_main():
    return render_template('profile/main.html', user=g.user)
