
import os

from datetime import date

import base64


class BaseConfig(object):
    # The name of the site used for internal sync, purely visual
    SITE_NAME = os.environ.get("SITE_NAME", "CORE Scouting")


    # Key used for encryption of site traffic. DO NOT SHARE
    # Generate a random url-safe base64 token from secrets
    SECRET_KEY = os.environ.get("SECRET_KEY", "Development")


    # Function for automatically updating the current year
    CURRENT_YEAR = lambda: date.today().year


    # The path or URL to the site's database, defaults to an in-memory only database if the env is not set
    # Should default to None, raising an error if not defined
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///scouting_site.sqlite")


    # API Key for accessing the FRC website api, used for specific team data and other information about the current season
    FRC_API_USERNAME = os.environ.get("FRC_API_USERNAME", "core2062")
    FRC_API_KEY = os.environ.get("FRC_API_KEY", "47744c35-3340-443d-bda0-632a18133b84")
    FRC_API_ENCODED_KEY = base64.b64encode(f"{FRC_API_USERNAME}:{FRC_API_KEY}".encode('ascii')).decode('ascii')


    # Used entirely for the current theme of the website, selectable themes can be found at bootswatch.com
    BOOTSTRAP_BOOTSWATCH_THEME = None

class DevelopmentConfig(BaseConfig):

    # Change the key to avoid issues with development env variables
    SECRET_KEY = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///scouting_dev.db"

class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = 'testing'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Move to fully in memory