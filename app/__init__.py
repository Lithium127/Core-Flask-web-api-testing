from flask import Flask, render_template, g, flash

import time
import requests

from . import config

from app.scouting.models import Competitions

from .database import db

from .assets import assets
from .extensions import bootstrap, csrf_protect

def register_extensions(app: Flask) -> None:
    """Registers all flask extensions to the app

    Args:
        app (Flask): Target Flask app
    """
    # apparently doing imports locally withing the function that
    # registers each extension can raise issues, most especially
    # with SQLAlchemy.
    db.init_app(app)

    assets.init_app(app)
    bootstrap.init_app(app)
    # csrf_protect.init_app(app)


from app.admin import admin
from app.frc_api import frc_api
from app.scouting import scouting
from app.site_info import site_info
from app.teams import teams

def register_blueprints(app: Flask) -> None:
    """Registers Flask Blueprints with the application

    Args:
        app (Flask): Target Flask app
    """
    app.register_blueprint(admin)
    app.register_blueprint(frc_api)
    app.register_blueprint(scouting)
    app.register_blueprint(site_info)
    app.register_blueprint(teams)



def register_commands(app: Flask) -> None:
    from app.commands import scout_data
    app.cli.add_command(scout_data)

    from app.admin.cli import admin_cli
    app.cli.add_command(admin_cli)

def register_error_handler(app: Flask) -> None:
    
    for status_code, error_message in {
        500: "Internal Server Error",
        404: "Page not found"
    }.items():
        @app.errorhandler(status_code)
        def error_handler(e):
            return render_template(f"errors/{status_code}.html", error = e, url_name = error_message), status_code

def create_app(config: config.BaseConfig = config.BaseConfig()) -> Flask:
    """Creates an instance of the CORE 2062 scouting site for use in a web application

    Args:
        config (BaseConfig, optional): Config to use. Defaults to BaseConfig().

    Returns:
        Flask: The finalized Flask application
    """

    app = Flask(__name__)

    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_error_handler(app)


    with app.app_context():
        db.create_all()
    
    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: f"{time.time() - g.request_start_time}s"

    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app



# place you code in the card body