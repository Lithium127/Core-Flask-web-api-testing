from flask import Blueprint

frc_api = Blueprint("frc", __name__, url_prefix="api/frc")

from . import views