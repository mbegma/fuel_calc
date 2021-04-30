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
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from fuel_calc_app.models import User


class RegisterForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=40)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=3, max=100)])
    # email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
