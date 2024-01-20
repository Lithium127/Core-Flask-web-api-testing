from flask import Blueprint

teams = Blueprint("teams", __name__, url_prefix="/teams")

from . import views