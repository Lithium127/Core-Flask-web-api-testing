
from flask import render_template, redirect, url_for, request

from . import scouting

from .models import Competitions, GameMatch, DataTranslation, Report, ReportData
from .forms import ScoutingDataForm

from app.database import db, select


@scouting.route("/")
def index():
    stmt = select(Competitions).where(Competitions.year == 2022)
    comp: Competitions = db.session.execute(statement=stmt).first()[0]
    match_schedule = comp.gamematch
    return render_template(
        'landing.html', 
        match_schedule = match_schedule,
        competition = comp
    )


@scouting.route("/report/<int:id>", methods=["GET","POST"])
def report(id):
    report_form = ScoutingDataForm()

    report: Report = db.session.execute(select(Report).where(Report.id == id)).first()[0]
    if report_form.validate_on_submit():
        report.dynamic_from_dict(data=report_form.data)
        report.save()
        return render_template("receipt.html", response_dict = report.dynamic_data.values())
    

    # set hidden variables to appropriate data
    report_form.match_number.data = report.gamematch.match_number
    report_form.position.data = report.position
    
    return render_template(
        "report.html",
        report = report,
        report_form = report_form
    )

