from flask import render_template

from . import teams

from app.database import db, select
from app.frc_api import api

from .models import Team

@teams.route("/")
def team_list():
    teams = db.session.execute(select(Team)).fetchall()

    return render_template("team_list.html", teams = teams)


@teams.route("/view/<int:id>")
def view_team(id: int):

    team = Team(id)
    return render_template(
        "team.html",
        team = team
    )

@teams.route("/fetch/frc/<int:id>")
def fetch_frc_data(id: int):
    """Makes calls to FRC API seperate from client DOM to smooth out loading times

    Args:
        id (int): Team number, from URL

    Returns:
        api.Team: A Team object containing response data
    """
    
    frc_data: api.Team = api.Team(id)

    return render_template("fetch/frc_data.html", team = frc_data)
