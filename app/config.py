
import os

from datetime import date


class BaseConfig(object):
    # The name of the site used for internal sync, purely visual
    SITE_NAME = os.environ.get("SITE_NAME", "CORE Scouting")

    # Key used for encryption of site traffic. DO NOT SHARE
    SECRET_KEY = os.environ.get("SECRET_KEY", None)

    # Function for automatically updating the current year
    CURRENT_YEAR = lambda: date.today().year

    # The path or URL to the site's database, defaults to an in-memory only database if the env is not set
    # Should default to None, raising an error if not defined
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", None)

    # API Key for accessing the FRC website api, used for specific team data and other information about the current season



class DevelopmentConfig(BaseConfig):

    # Change the key to avoid issues with development env variables
    SECRET_KEY = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = 'testing'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Move to fully in memory