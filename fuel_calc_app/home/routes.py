# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: fuel_calc
# Name: routes
# Filename: routes.py
# Author: mbegma
# Create data: 27.04.2021
# Description: 
# Copyright: (c) Дата+, 2021
# -----------------------------------------------------
from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['GET'])
def home():
    # homepage
    return render_template(
        'index.jinja2',
        title='Title Page',
        subtitle='demonstration',
        template='home-template'
    )
