from flask import Blueprint

site_info = Blueprint("site_info", __name__, template_folder='templates')

from . import views