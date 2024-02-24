from flask import Flask, render_template, g, flash

import time

from . import config

from app.scouting.models import Competitions

def register_extensions(app: Flask) -> None:
    """REgisters all flask extensions to the app

    Args:
        app (Flask): Target Flask app
    """
    from .database import db
    db.init_app(app)

    from .assets import assets
    assets.init_app(app)

    from .extensions import bootstrap, csrf_protect
    bootstrap.init_app(app)
    csrf_protect.init_app(app)



def register_blueprints(app: Flask) -> None:
    """Registers Flask Blueprints with the application

    Args:
        app (Flask): Target Flask app
    """
    
    from app.scouting import scouting
    app.register_blueprint(scouting)

    from app.teams import teams
    app.register_blueprint(teams)

    from app.site_info import site_info
    app.register_blueprint(site_info)
    
    from app.frc_api import frc_api
    app.register_blueprint(frc_api)

    from app.admin import admin
    app.register_blueprint(admin)



def register_commands(app: Flask) -> None:
    from app.commands import scout_data
    app.cli.add_command(scout_data)

    from app.admin.cli import admin_cli
    app.cli.add_command(admin_cli)



def create_app(config: config.BaseConfig = config.DevelopmentConfig()) -> Flask:
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

    from .database import db
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