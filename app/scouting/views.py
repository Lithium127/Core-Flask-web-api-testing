
from flask import render_template

from . import scouting

from .models import GameMatch, DataTranslation, Report, ReportData


@scouting.route("/")
def index():
    return render_template('landing.html', match_schedule = [])


# API endpoint for sending data to.
@scouting.route("/report", methods=["GET", "POST"])
def report():
    return "Scouting Post request"
