from flask import render_template, request

from . import frc_api
from . import api


@frc_api.route("/view-event/<int:id>")
def view_event(id: int):
    events = api.Events(tournement_type="Regional")
    
    return render_template("event.html", event = events.event_list[id])

@frc_api.route("/get_event_schedule", methods=["POST"])
def render_event_schedule():
    data = request.form
    event_code = data["eventCode"]
    year = data["year"] or None
    level = data["level"] or 'qual'
    schedule = api.EventSchedule(
        event_code=event_code,
        year=year,
        tournament_level=level
    )