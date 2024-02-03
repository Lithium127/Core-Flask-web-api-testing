import pytest

from app.frc_api import api

from app import create_app, config
from datetime import date

@pytest.fixture()
def app():
    app = create_app(config=config.TestingConfig)
    yield app

def test_root_api(app):
    with app.app_context():
        rootcall = api.RootCall()

    normal_headers = {
        "currentSeason": date.today().year,
        "maxSeason": date.today().year,
        "name": "FIRST ROBOTICS COMPETITION API",
        "apiVersion": "3.0",
        "status": "normal"
    }

    response_data = rootcall.response.json()

    for key in normal_headers:
        assert normal_headers[key] == response_data[key]
    
    assert rootcall.status == 200

def test_season_summary(app):
    with app.app_context():
        season = api.SeasonSummary(2023)
    
    assert season.status == 200
    assert season.json != {}


def test_events(app):
    with app.app_context():
        events = api.Events(2023, week_number=2)
    
    assert len(events.event_list) == events.event_count
    assert len(events.event_list) > 0


def test_team_season(app):
    with app.app_context():
        schedule = api.Events(2024, team_number=2062)
    
    print(schedule.json)
    
def test_team(app):
    with app.app_context():
        team = api.Team(2062)
    
    print(team.info)