from flask import Blueprint

mod_main = Blueprint('mod_main', __name__)

from . import views