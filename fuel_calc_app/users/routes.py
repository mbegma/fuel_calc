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
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm, AddCarForm, EditProfileForm
from fuel_calc_app.models import User, Car
from fuel_calc_app import db

# Blueprint configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# @user_bp.route('/user/<username>')
# @login_required
# def user(username):
#     u = User.query.filter_by(username=username).first_or_404()
#     cars = [
#         {'car_name': 'car name #1', 'car_model': 'Car model #1'},
#         {'car_name': 'car name #2', 'car_model': 'Car model #2'},
#     ]
#     return render_template('user.html', user=user, posts=cars)


@user_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@user_bp.route('/profile/<username>')
@login_required
def profile(username):
    u = User.query.filter_by(user_name=username).first_or_404()
    cars = [
        {'car_name': 'car name #1', 'car_model': 'Car model #1'},
        {'car_name': 'car name #2', 'car_model': 'Car model #2'}
    ]
    return render_template(
        'profile.jinja2',
        title='Profile Page',
        subtitle='user profile',
        template='users-template',
        user=u, cars=cars
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
        return redirect(url_for('user_bp.profile', username=new_user.user_name))
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
        return redirect(url_for('user_bp.profile', username=current_user.user_name))

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
                return redirect(url_for('user_bp.profile', username=user.user_name))

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
    u = current_user
    u.authenticated = False
    db.session.add(u)
    db.session.commit()
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('home_bp.home'))


@user_bp.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    form = AddCarForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_car = Car(car_name=form.car_name.data,
                      car_model=form.car_model.data,
                      car_year=form.car_year.data,
                      is_default_car=form.car_default.data,
                      user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        flash('Автомобиль {} добавлен в гараж !'.format(new_car.name))
        return redirect(url_for('user_bp.profile', username=current_user.user_name))
    return render_template(
        'add_car.jinja2',
        title='Add Car Page',
        subtitle='add car',
        template='users-template',
        form=form)


@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        current_user.gender = form.gender.data

        # return form.dt.data.strftime('%Y-%m-%d')
        current_user.birthday = form.birthday.data  # .strftime('%Y-%m-%d')
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user_bp.profile', username=current_user.user_name))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
        form.gender.data = current_user.gender
        form.birthday = current_user.birthday
    return render_template(
        'edit_profile.jinja2',
        title='Edit User Profile',
        template='users-template',
        form=form)

