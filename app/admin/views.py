from flask import render_template, request, redirect, url_for

from datetime import date

from . import admin
from .form import CreateEventForm

from app.frc_api import api



@admin.route("/")
def index():
    create_event_form = CreateEventForm()
    return render_template("admin_home.html", create_event_form = create_event_form)


@admin.route("/database")
def database():
    return "WIP"


@admin.post("/fetch/event-schedule")
def render_event_schedule():
    data = request.get_json()
    event_code = data.get("eventCode", None)
    if event_code is None or len(event_code) < 4:
        return "<h1>No event found</h1>" # really bad error handling :(
    
    year = data.get("year", date.today().year)
    level = data.get("level", "qual")

    error = ""
    
    try:
        schedule = api.EventSchedule(event_code=event_code,year=year,tournament_level=level).schedule
    except api.FRCAPIError:
        schedule = []
        error = f"No event {event_code} in year {year}"
    
    return render_template("fetch/event_schedule.html", schedule = schedule, error = error)

@admin.route("/create_event", methods=['GET', 'POST'])
def create_event():
    return redirect(url_for("admin"))