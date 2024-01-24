import pytest

from app import create_app, config
from app.scouting.models import Report

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



def test_request_index(client):
    """Checks to make sure the app can route to its home page

    Args:
        client (_type_): _description_
    """
    response = client.get("/")
    assert b"Hello World!" in response.data


def test_database_report(app):
    with app.app_context():
        report = Report(
            "John Doe",
            6,
            "2062",
            {
                "hover":10
            }
        )
    