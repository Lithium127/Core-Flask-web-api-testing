from flask import Flask, render_template

from . import config

def register_extensions(app: Flask) -> None:
    """REgisters all flask extensions to the app

    Args:
        app (Flask): Target Flask app
    """
<<<<<<< HEAD

=======
>>>>>>> a4085f2 (Created Base Index)
    from .database import db
    db.init_app(app)

    from .assets import assets
    assets.init_app(app)

def register_blueprints(app: Flask) -> None:
    """Registers Flask Blueprints with the application

    Args:
        app (Flask): Target Flask app
    """
    
    from app.scouting import scouting
    app.register_blueprint(scouting)

    from app.teams import teams
    app.register_blueprint(teams)

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

    from .database import db
    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app