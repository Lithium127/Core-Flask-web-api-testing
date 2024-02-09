from flask import render_template, request

from datetime import date

from . import admin

from app.frc_api import api

@admin.route("/")
def index():
    return render_template("admin_home.html")


@admin.route("/database")
def database():
    return "WIP"


@admin.route("/fetch/event-schedule")
def render_event_schedule():
    event_code = request.args.get("eventCode", None)

    if event_code is None:
        return "<h1>No event found</h1>" # really bad error handling :(
    
    year = request.args.get("year", date.today().year)
    level = request.args.get("level", "qual")

    event = api.EventSchedule(
        event_code=event_code,
        year=year,
        tournament_level=level
    )
    
    return render_template("fetch/event_schedule.html", event = event)