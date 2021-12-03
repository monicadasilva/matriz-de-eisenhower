from flask import  Flask
from app.routes.categories_routes import bp_cat
from app.routes.tasks_routes import bp_task


def init_app(app: Flask):
    app.register_blueprint(bp_task)
    app.register_blueprint(bp_cat)