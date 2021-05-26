# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: flask_base_structure_1
# Name: forms
# Author: mbegma
# Create data: 29.03.2018
# Description: 
# Copyright: (c) Дата+, 2018
# -----------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from fuel_calc_app.models import User


class RegisterForm(FlaskForm):
    user_name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=40)])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    user_name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=100)])
    # email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Помнить меня')
    submit = SubmitField('Войти')


class AddCarForm(FlaskForm):
    car_name = StringField('Название машины', validators=[DataRequired(), Length(min=1, max=128)])
    car_model = StringField('Модель', validators=[DataRequired(), Length(min=1, max=128)])
    car_year = IntegerField('Год выпуска')
    car_default = BooleanField('Машина по умолчанию')
    submit = SubmitField('Добавить')


class EditProfileForm(FlaskForm):
    user_name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=255)])
    location = StringField('Location', validators=[Length(min=0, max=128)])
    gender = StringField('Gender', validators=[Length(max=32)])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    submit = SubmitField('Обновить')
