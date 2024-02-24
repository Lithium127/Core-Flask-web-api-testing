import click

from flask.cli import AppGroup, with_appcontext

from app.database import db
from app.scouting.models import Competitions, GameMatch
from app.database import select, db

scout_data = AppGroup("scout-data")

@scout_data.command("display-table")
@click.argument("year")
def display_table(year: int):
    stmt = select(GameMatch)
    result = db.session.execute(stmt).fetchall()
    click.echo(result)
    def result_dict(r):
        return dict(zip(r.keys(), r))
    #click.echo(list(map(result_dict, result)))