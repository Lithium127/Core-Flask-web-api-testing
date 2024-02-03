from flask import Blueprint

frc_api = Blueprint("frc", __name__, url_prefix="/api/frc", template_folder="templates")

from . import views