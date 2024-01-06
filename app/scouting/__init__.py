from flask import Blueprint

scouting = Blueprint("scouting", __name__)

from . import views