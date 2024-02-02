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
    
    print(rootcall.response.json())

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
    
    print(season.response.json())