from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from MyWebsite import db, login_manager
from MyWebsite.mod_auth.forms import LoginForm, SignupForm
from MyWebsite.mod_auth.models import User
from flask_login import LoginManager, login_user

mod_auth = Blueprint('auth',__name__, url_prefix='/auth')

'''
The @login_manager.user_loader piece tells Flask-login how to load users 
given an id.
'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(email=user_id)

@login_manager.request_loader
def load_request(request):
    email = 
    return 

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.session.query(User.email).filter_by(email=login_form.user_name.data).first()
        if user is None:
            login_form.user_name.errors('Invalid username') 
        else:
            # log the user *in* :)
            if not user.check_password(login_form.password.data):
                # Incorrect password :(
                # TODO: FIXME: implement brute force protection
                login_form.password.errors('Invalid password')
            else:
                # Yay! User information is correct
                flask.flash('Logged in successfully.')
                return redirect(url_for('home'))

    return render_template('auth/login.html', form=form)

@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        # Check whether the user name is unique
        user_name_taken = db.session.query(User.email).filter_by(email=form.user_name.data).scalar() is not None
        if user_name_taken:
            form.user_name.errors.append('Username taken')
        else:
            user = User(form.user_name.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering')
            # TODO send email to the user for registration signup
            login_user(user.email, remember=True)
            return redirect(url_for('home'))
    return render_template('auth/signup.html', form=form)


'''
 @@ TODO: Integration with Facebook.
'''
# Integrate with facebook o-auth

# store auth-token from FB into database

# create test accounts to ensure everything works: https://developers.facebook.com/apps/{YOUR_APP_ID}/roles/test-users/), 