"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect
from flask import current_app as app
from flask_login import login_required
from flask_mail import Mail, Message
from AlertWeb.mod_auth.models import User
from AlertWeb import mail
from . import mod_main

@mod_main.route('/')
@mod_main.route('/home')
def home():
    """Renders the home page."""
    print("home function*******")
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
    
@mod_main.route('/contact')
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

@mod_main.route('/testmail')
def test_mail():
    """Send's a test email."""
    msg = Message(app.config['ALERT_WEB_MAIL_SUBJECT_PREFIX'] + "hello",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=["deelaws89@gmail.com", "deelaws@hotmail.com"])
    msg.body = "testing"
    mail.send(msg)
    flash('Successfully sent test mail')
    return redirect(url_for('mod_main.home'))

@mod_main.route('/about')
@login_required
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@mod_main.route('/profile')
@login_required
def profile_main():
    return render_template('profile/main.html', user=g.user)
