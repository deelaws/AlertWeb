from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from AlertWeb import db, login_manager
from AlertWeb.mod_auth.forms import LoginForm, SignupForm
from AlertWeb.mod_auth.models import User
from flask_login import LoginManager, login_user, logout_user

mod_auth = Blueprint('auth',__name__, url_prefix='/auth')

'''
The @login_manager.user_loader piece tells Flask-login how to load users 
given an id.
'''
@login_manager.user_loader
def load_user(user_id):
    print("Load_user*******")
    print(user_id)
    return User.query.filter_by(email=user_id).first()

''' https://flask-login.readthedocs.io/en/latest/#custom-login-using-request-loader
@login_manager.request_loader
def load_request(request):
    print("**** call to load request *****")
    return None
    '''

'''
LOGIN VIEW
'''
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        user = User.query.filter_by(email=login_form.user_name.data).first()
        if user is None:
            login_form.user_name.errors.append('Invalid Username or password') 
        else:
            # log the user *in* :)
            print(user.email)
            print(type(user))
            if not user.check_password(login_form.password.data):
                # Incorrect password :(
                # TODO: FIXME: implement brute force protection a.k.a  rate limiting
                login_form.password.errors.append('Invalid Username or password')
            else:
                # Yay! User information is correct
                flash('Logged in successfully.')
                login_user(user, remember=True)
                return load_main_page(user)
    return render_template('auth/login.html', form=login_form)

'''
LOGOUT VIEW
'''
@mod_auth.route('/logout', methods=['GET', 'POST'])
def logout():
    flash('Logged out successfully.')
    logout_user()
    return redirect(url_for('home')) 

'''
SIGNUP VIEW
'''
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
            return redirect(url_for('home'))
    return render_template('auth/signup.html', form=form)


def load_main_page(user):
    return render_template('profile/main.html', user=user)

'''
 @@ TODO: Integration with Facebook.
'''
# Integrate with facebook o-auth

# store auth-token from FB into database

# create test accounts to ensure everything works: https://developers.facebook.com/apps/{YOUR_APP_ID}/roles/test-users/), 