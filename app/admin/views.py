from flask import render_template, request, redirect, url_for, jsonify

from datetime import date

from . import admin


from app.frc_api import api

from .forms import CreateNewCompetitionForm, RequestFieldYearForm
from app.scouting.models import Competitions

@admin.route("/", methods=["GET","POST"])
def index():
    create_event_form = CreateNewCompetitionForm() # used only for fetch request csrf token
    

    if create_event_form.validate_on_submit():
        error = ""

        event = api.EventSchedule(
            event_code=create_event_form.event_code.data,
            year=create_event_form.year.data,
            tournament_level=create_event_form.event_type.data,
            defer=True
        )
        try:
            event._make_request()
            schedule = event.schedule
        except api.FRCAPIError as e:
            schedule = []
            error = f"{e.__class__.__name__}: {e}\nURL Target: {event.target_url}"
        
        return render_template("fetch/event_schedule.html", schedule = schedule, error = error)

    if request.method == "GET":
        # only return the full page if the request is from a client and not fetch
        return render_template(
            "admin_home.html", 
            create_event_form = create_event_form
        )
    
    return "Error"

@admin.route("/create-event", methods=["POST"])
def create_event():
    form = CreateNewCompetitionForm()

    if form.validate_on_submit():
        c = Competitions.create_from_frc(
            event_code=form.event_code.data,
            year=form.year.data,
            tournament_level=form.event_type.data
        ).save()
        return "FORM VALIDATED"
    
    return redirect(url_for("scouting.index"))


@admin.route("/database")
def database():
    return "WIP"



@admin.route("edit-fields", methods=["GET", "POST"])
def edit_form_fields():
    form = RequestFieldYearForm()
    if form.validate_on_submit():
        name = form.name.data
        return render_template("fetch/fields_table.html")
    return render_template("edit_fields.html", form = form)
