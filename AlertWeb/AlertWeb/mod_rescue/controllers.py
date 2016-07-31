from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required
from AlertWeb import db
from AlertWeb.mod_rescue.forms import CreateRescueAlertForm
from AlertWeb.mod_rescue.models import RescueAlert
from AlertWeb.mod_rescue.adventure_type import *
from AlertWeb.mod_auth.models import User

from datetime import datetime

# Contoller = view

mod_resc_alert = Blueprint('rescue_alert',__name__, url_prefix='/rescue')

def convert_client_time(time):
    return datetime.strptime(time, '%m/%d/%Y %I:%M %p')

'''
Creates a rescue alert for the current user
'''
@mod_resc_alert.route('/create', methods=['GET', 'POST'])
@login_required
def create_rescue_alert():
    form = CreateRescueAlertForm(request.form)
    print("============================data=================================")
    print(form)
    print(form.adventure_start_time.data)
    print(form.adventure_start_time)
    print(form.adventure_start_time.raw_data)
    print("=============================================================")
    if request.method == 'POST':
        print("FORM is VALIDATED")
        alert = RescueAlert(form.adventure_name.data,
                            form.adventure_type.data,
                            convert_client_time(form.adventure_start_time.raw_data[0]),
                            form.adventure_end_date.data)
        user = g.user
        user.rescue_alerts.append(alert)
        db.session.add(user)
        db.session.commit()
        flash('Successfully create a Rescue Alert!')
        return redirect(url_for('home'))
    return render_template("rescue/create_alert.html", form=form)

'''
List's the rescue alerts for the current user
'''
@mod_resc_alert.route('/list', methods=['GET'])
@login_required
def list_rescue_alert():
    alerts = g.user.rescue_alerts
    return render_template("rescue/list_alerts.html", alerts=alerts, user=g.user)

