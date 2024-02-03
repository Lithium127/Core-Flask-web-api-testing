from flask import Flask, render_template, g, flash

import time

from . import config

def register_extensions(app: Flask) -> None:
    """REgisters all flask extensions to the app

    Args:
        app (Flask): Target Flask app
    """
    from .database import db
    db.init_app(app)

    from .assets import assets
    assets.init_app(app)
    
    from app.extensions import bootstrap
    bootstrap.init_app(app)

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

def register_commands(app: Flask) -> None:
    from app.commands import scout_data
    app.cli.add_command(scout_data)

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