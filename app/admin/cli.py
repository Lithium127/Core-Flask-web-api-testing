import click

from flask import current_app
from flask.cli import AppGroup

from sqlalchemy import func

from app.database import db, select
from app.frc_api import api

from app.scouting.models import Competitions

from datetime import date


admin_cli = AppGroup("admin")

@admin_cli.command("create-event")
@click.option("--level", default=0, help="Event level to select. 0 = qual, 1 = playoff")
@click.argument("event-id")
@click.argument("year", default=date.today().year)
def echo(level, event_id, year):
    try:
        with current_app.app_context():
            event = api.EventSchedule(
                event_code=event_id,
                year=year,
                tournament_level=["qual","playoff"][level],
                defer=True
            )
            click.echo(f"Target: {event.target_url}\nMaking request to FRC API...")
            event._make_request()
    except api.FRCAPIError as e:
        if event.status == 404:
            raise click.exceptions.ClickException(f"No {event.level} matches found for event {event.event_code}")
        raise click.BadArgumentUsage(f"An error was caused in API request:\n{e.__class__.__name__}: {e}")
    
    click.echo(f"\t--=[\t{event.event_code}-{event.year}\t{event.level}\t]=--")
    click.echo("#\tRed 1\tRed 2\tRed 3\tBlue 1\tBlue 2\tBlue 3\n-----")
    for index, match in enumerate(event.schedule):
        if index >= 20:
            break
        line = []
        line.append(match["description"].split(" ")[-1])
        for team in match["teams"]:
            line.append(str(team["teamNumber"]))
        click.echo("\t".join(line))
    click.echo("-----")
    if year != date.today().year:
        click.echo("[WARNING] : This event is not for the current year")
    confirm = input("Create table [Y/N]: ")
    if confirm.lower() == "y":
        comp = Competitions.create_from_event(event)
        click.echo(comp.save())
        click.echo("Created new table")
    else:
        raise click.Abort()

@admin_cli.command("get-table-rows")
def get_table_rows():
    rows = db.session.query(func.count(Competitions.id)).scalar()
    click.echo(f"Number or rows: {rows}")