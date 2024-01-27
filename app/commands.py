import click

from flask.cli import AppGroup, with_appcontext

from app.database import db
from app.scouting.models import GameMatch

scout_data = AppGroup("scout-data")


@scout_data.command("generate-gamematch")
@click.argument("count", type=int)
@with_appcontext
def generate_gamematch(count: int):
    for _ in range(count):
        db.session.add(GameMatch())
    db.session.commit()
    click.echo(f"Added {count} rows to GameMatch table")


@scout_data.command("display-table")
@click.argument("table-name", type=str)
def display_table(table_name: str):
    click.echo("Not implemented")