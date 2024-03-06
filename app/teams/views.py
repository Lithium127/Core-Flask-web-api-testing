from flask import render_template

from . import teams

from app.database import db, select

from .models import Team

@teams.route("/")
def team_list():
    teams = db.session.execute(select(Team)).fetchall()

    return render_template("team_list.html", teams = teams)


@teams.route("/view/<int:id>")
def view_team(id: int):
    team = Team(2062)
    return render_template("team.html", team = team)