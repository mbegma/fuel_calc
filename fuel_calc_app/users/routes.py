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
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm
from fuel_calc_app.models import User
from fuel_calc_app import db

# Blueprint configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@user_bp.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.jinja2',
        title='Profile Page',
        subtitle='user profile',
        template='users-template'
    )


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If the User is already logged in, don't allow them to try to register
    if current_user.is_authenticated:
        flash('Already registered!  Redirecting to your User Profile page...')
        return redirect(url_for('user_bp.profile'))

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(form.user_name.data, form.email.data, form.password.data)
        new_user.authenticated = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Thanks for registering, {}!'.format(new_user.email))
        return redirect(url_for('user_bp.profile'))
    return render_template(
        'register.jinja2',
        title='Register Page',
        subtitle='user register',
        template='users-template',
        form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If the User is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!  Redirecting to your User Profile page...')
        return redirect(url_for('user_bp.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # user = User.query.filter_by(email=form.email.data).first()
            user = User.query.filter_by(user_name=form.user_name.data).first()
            if user and user.is_correct_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                flash('Thanks for logging in, {}!'.format(current_user.email))
                return redirect(url_for('user_bp.profile'))

        flash('ERROR! Incorrect login credentials.')
    return render_template(
        'login.jinja2',
        title='Login Page',
        subtitle='user login',
        template='users-template',
        form=form)


@user_bp.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('home_bp.home'))

