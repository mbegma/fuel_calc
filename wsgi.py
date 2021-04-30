# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: fuel_calc
# Name: wsgi
# Filename: wsgi.py
# Author: mbegma
# Create data: 27.04.2021
# Description: 
# Copyright: (c) Дата+, 2021
# -----------------------------------------------------
from fuel_calc_app import create_app
# from fuel_calc_app.models import User, Car

app = create_app()


# @app.shell_context_processors
# def make_shell_context():
#     return {'db': db, 'User': User, 'Car': Car}


if __name__ == "__main__":
    app.run(host='0.0.0.0')

