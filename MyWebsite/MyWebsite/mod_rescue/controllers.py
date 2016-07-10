from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required
from MyWebsite import db
from MyWebsite.mod_rescue.forms import CreateRescueAlertForm
from MyWebsite.mod_rescue.models import RescueAlert
from MyWebsite.mod_rescue.adventure_type import *
from MyWebsite.mod_auth.models import User

# Contoller = view

mod_resc_alert = Blueprint('rescue_alert',__name__, url_prefix='/rescue')

'''
Creates a rescue alert for the current user
'''
@mod_resc_alert.route('/create', methods=['GET', 'POST'])
@login_required
def create_rescue_alert():
    form = CreateRescueAlertForm(request.form)
    if request.method == 'POST' and form.validate():
        alert = RescueAlert(form.adventure_name.data,
                            form.adventure_type.checked,
                            form.adventure_start_time.data,
                            form.adventure_end_time.data)
        user = g.user
        user.rescue_alerts.append(alert)
        db.session.add(user)
        db.session.commit()
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

