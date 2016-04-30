"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from MyWebsite import app

def function():
	print('afadsfd')


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    #ab = 1, 2
    #print("a={0},b={1}".format(a, b))
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
