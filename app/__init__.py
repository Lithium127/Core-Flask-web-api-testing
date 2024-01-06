from flask import Flask

from .config import BaseConfig

def register_extensions(app: Flask) -> None:
    """REgisters all flask extensions to the app

    Args:
        app (Flask): The target app
    """
    from .database import db

    db.init_app(app)

def register_blueprints(app: Flask) -> None:
    """Registers all blueprints to the Flask object app

    Args:
        app (Flask): The target app
    """
    from .teams import teams
    app.register_blueprint(teams, url_prefix = "/teams")

def create_app(config: BaseConfig = BaseConfig()) -> Flask:
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

    @app.route("/")
    def index():
        return "Hello World!"
    
    return app