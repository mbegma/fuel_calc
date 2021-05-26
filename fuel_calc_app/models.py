# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: flask_base_structure_1
# Name: models
# Author: mbegma
# Create data: 29.03.2018
# Description: 
# Copyright: (c) Дата+, 2018
# -----------------------------------------------------
# команды миграции:
# \flask db migrate - создает сценарий миграции по текущим данным модели
# \flask db migrate -m "users table"
#
# \flask db upgrade - выполняется миграция (применение изменений в базе данных по ранее созданному сценарию)
# \flask db downgrade - отменяет последнюю миграцию
# \flask db stamp head - указывают, что текущее состояние базы данных отражает применение всех миграций
# -----------------------------------------------------
# from app import db, bcrypt
from fuel_calc_app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, nullable=True)
    cars = db.relationship('Car', backref='user', lazy='dynamic')
    # role = db.Column(db.String, default='user')
    about_me = db.Column(db.String(255))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(128))
    gender = db.Column(db.String(32))
    birthday = db.Column(db.DateTime)

    def __init__(self, user_name, email, plaintext_password):
        self.user_name = user_name
        self.email = email
        self.password_hash = generate_password_hash(plaintext_password)
        self.registered_on = datetime.now()
        # self.role = role

    def set_password(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password)

    def is_correct_password(self, plaintext_password):
        return check_password_hash(self.password_hash, plaintext_password)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    model = db.Column(db.String(128))
    car_year = db.Column(db.Integer)
    is_default_car = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, car_name, car_model, car_year, is_default_car, user_id):
        self.name = car_name
        self.model = car_model
        self.car_year = car_year
        self.is_default_car = is_default_car
        self.user_id = user_id
        self.added_date = datetime.now()

    def __repr__(self):
        return '<Car {}>'.format(self.name)
