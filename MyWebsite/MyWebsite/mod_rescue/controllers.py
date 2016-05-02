from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from MyWebsite import db
from MyWebsite.mod_rescue.forms import CreateRescueAlertForm
from MyWebsite.mod_rescue.models import RescueAlert
from MyWebsite.mod_rescue.adventure_type import *

# Contoller = view

mod_resc_alert = Blueprint('rescue_alert',__name__, url_prefix='/rescue')

# Set the create rescue alert function
@mod_resc_alert.route('/create', methods=['GET', 'POST'])
def create_rescue_alert():
    form = CreateRescueAlertForm(request.form)
    if request.method == 'POST' and form.validate():
        alert = RescueAlert(form.adventure_name.data,
                            int_to_adventure_type(0),
                            form.adventure_start_time.data,
                            form.adventure_end_time.data)
        db.session.add(alert)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("rescue/create_alert.html", form=form)

