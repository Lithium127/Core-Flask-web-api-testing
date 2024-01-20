
from flask import render_template

from . import scouting



@scouting.route("/")
def index():
    return render_template('landing.html')


# API endpoint for sending data to.
@scouting.route("/report", methods=["GET", "POST"])
def report():
    return "Scouting Post request"
