from flask import Blueprint

scouting = Blueprint("scouting", __name__, url_prefix="/scouting", template_folder="templates")

from . import views