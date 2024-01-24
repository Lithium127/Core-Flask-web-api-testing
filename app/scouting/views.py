from . import scouting

from .models import GameMatch, DataTranslation, Report, ReportData


@scouting.route("/")
def index():
    return "Scouting"


# API endpoint for sending data to.
@scouting.route("/report", methods=["POST"])
def report():
    return "Scouting Post request"