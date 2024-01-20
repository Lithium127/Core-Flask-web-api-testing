from flask import Flask

from .config import BaseConfig

def register_extensions(app: Flask) -> None:
    from .database import db

    db.init_app(app)

def register_blueprints(app: Flask) -> None:

    from app.scouting import scouting
    app.register_blueprint(scouting)

def create_app(config: BaseConfig = BaseConfig()) -> Flask:

    app = Flask(__name__)

    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    @app.route("/")
    def index():
        return "Hello World!"
    
    return app