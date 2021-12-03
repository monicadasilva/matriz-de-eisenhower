from flask import Flask
from os import getenv
from dotenv import load_dotenv
from app import routes
from app.configs import migration, database


load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
    app.config["JSON_SORT_KEYS"] = False

    database.init_app(app)
    migration.init_app(app)
    routes.init_app(app)
    

    return app