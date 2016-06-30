"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from MyWebsite import app
from flask_login import login_required
from MyWebsite.mod_auth.models import User

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
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
    user_name = session['user_id']
    user = User.query.filter_by(email=user_name).first()
    return render_template('profile/main.html', user=user)
