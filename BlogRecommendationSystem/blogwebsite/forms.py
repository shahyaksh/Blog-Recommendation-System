from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from blogwebsite import api_link
import requests


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        result = requests.get(f"{api_link}/name/{username.data}").text
        if result == "not unique":
            raise ValidationError('This Username already exists.Please select a different one')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', render_kw={'readonly': True})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if session["name"] != username.data:
            result = requests.get(f"{api_link}/name/{username.data}").text
            if result == "not unique":
                raise ValidationError('This Username already exists.Please select a different one')
