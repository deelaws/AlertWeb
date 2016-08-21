from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from flask import current_app as alert_app

from flask_mail import Mail, Message
from flask_login import login_required
from AlertWeb import db, mail
from AlertWeb.mod_rescue.forms import CreateRescueAlertForm
from AlertWeb.mod_rescue.models import RescueAlert
from AlertWeb.mod_rescue.adventure_type import *
from AlertWeb.mod_auth.models import User

from datetime import datetime

# Contoller = view

mod_resc_alert = Blueprint('rescue_alert',__name__, url_prefix='/rescue')

def convert_client_time(time):
    return datetime.strptime(time, '%m/%d/%Y %I:%M %p')


def send_alert_created_mail(subject, recipient, **kwargs):
    msg = Message(alert_app.config['ALERT_WEB_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=alert_app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = render_template('rescue/create_rescue_mail' + '.txt', **kwargs)
    msg.html = render_template('rescue/create_rescue_mail' + '.html', **kwargs)
    mail.send(msg)
    print("MAIL Sent")

'''
Creates a rescue alert for the current user
'''
@mod_resc_alert.route('/create', methods=['GET', 'POST'])
@login_required
def create_rescue_alert():
    form = CreateRescueAlertForm(request.form)
    print("======================")
    print(form.adventure_name.data)
    print(form.adventure_start_time.data)
    print(form.adventure_start_time.raw_data)
    print(form.adventure_end_time.data)
    print(form.adventure_end_time.raw_data)
    if request.method == 'POST' and form.validate():
        print("FORM is VALIDATED")
        alert = RescueAlert(form.adventure_name.data,
                            form.adventure_type.data,
                            convert_client_time(form.adventure_start_time.raw_data[0]),
                            convert_client_time(form.adventure_end_time.raw_data[0]))
        user = g.user
        user.rescue_alerts.append(alert)
        db.session.add(user)
        db.session.commit()
        flash('Successfully create a Rescue Alert!')
        #send_alert_created_mail("Rescue Alert Created", user.email, ralert=alert)
        return redirect(url_for('mod_main.home'))
    return render_template("rescue/create_alert.html", form=form)

'''
List's the rescue alerts for the current user
'''
@mod_resc_alert.route('/list', methods=['GET'])
@login_required
def list_rescue_alerts():
    alerts = g.user.rescue_alerts
    return render_template("rescue/list_alerts.html", alerts=alerts, user=g.user)