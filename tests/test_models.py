import pytest

from app import create_app, config

from app.database import db

from app.scouting.models import Report, GameMatch, DataTranslation, ReportData

@pytest.fixture()
def app():
    app = create_app(config=config.TestingConfig)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_gamematch_report(app):
    with app.app_context():
        game_match = GameMatch()
        game_match.reports[0].__init__(
            "John Doe",
            1,
            2062,
            {},
            "These are comments"
        )
        game_match.save()

        assert len(game_match.reports) == 6
        assert game_match.reports[0].reporter == "John Doe"

def test_translation_table(app):
    with app.app_context():
        translation_table = DataTranslation.add_keys(
            {
                "bool_01":bool,
                "bool_02":True,
                "int_01":int,
                "int_02":0,
                "str_01":str,
                "str_02":""
            }
        )
        game_match = GameMatch()
        game_match.add_report(Report(
            "John Doe",
            2,
            2062,
            {
                "bool_01":True,
                "bool_02":True,
                "int_01":12,
                "str_01":"this is a test"
            },
            "These are comments"
        ))

def test_dynamic_report(app):
    with app.app_context():
        pass