from flask import Flask
from sqlalchemy import create_engine, MetaData

import spacy

import os

# Database stuff
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
engine = create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
metadata = MetaData()

# Spacy stuff
nlp = spacy.load('en_core_web_sm')


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .db_structure_tree.routes import db_structure
    from .search.routes import search
    from .main.routes import main
    from .errors.handlers import errors

    app.register_blueprint(db_structure)
    app.register_blueprint(search)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
