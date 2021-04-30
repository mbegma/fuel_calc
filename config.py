# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: fuel_calc
# Name: config
# Filename: config.py
# Author: mbegma
# Create data: 27.04.2021
# Description: 
# Copyright: (c) Дата+, 2021
# -----------------------------------------------------
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = 'wsgi.py'

    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = True
    LESS_RUN_IN_DEBUG = True

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = True

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' + path.join(basedir, 'fuel_calc_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


