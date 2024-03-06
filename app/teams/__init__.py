from flask import Blueprint

teams = Blueprint("teams", __name__, url_prefix="/teams", template_folder="templates/")

from . import views