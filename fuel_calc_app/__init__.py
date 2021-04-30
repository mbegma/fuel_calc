# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: fuel_calc
# Name: __init__.py
# Filename: __init__.py
# Author: mbegma
# Create data: 27.04.2021
# Description: 
# Copyright: (c) Дата+, 2021
# -----------------------------------------------------
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt

bootstrap = Bootstrap()
login = LoginManager()
login.login_view = "user_bp.login"
db = SQLAlchemy()
migrate = Migrate()
# bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    bootstrap.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # bcrypt.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .home import home
        from .users import user

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(user.user_bp)

        return app

