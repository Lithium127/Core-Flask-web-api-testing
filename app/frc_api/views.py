from flask import render_template

from . import frc_api
from . import api


@frc_api.route("/view-event/<int:id>")
def view_event(id: int):
    events = api.Events(tournement_type="Regional")
    
    return render_template("event.html", event = events.event_list[id])