from flask import Flask
from sqlalchemy import create_engine

import os

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
engine = create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .db_structure_tree.routes import posts
    from .main.routes import main
    from .errors.handlers import errors

    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
