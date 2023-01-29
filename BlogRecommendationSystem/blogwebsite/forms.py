from cgitb import reset
from unittest import result
from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blogwebsite import mysql

conn = mysql.connect()
cursor = conn.cursor()


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        cursor.execute(''' SELECT user_name from User_Profile 
                                        where user_name=%s''', [username.data])
        result = cursor.fetchone()
        if result:
            raise ValidationError('This Username already exists.Please select a different one')

    def validate_email(self, email):
        cursor.execute(''' SELECT user_email from User_Profile 
                                        where user_email=%s''', [email.data])
        result = cursor.fetchone()
        if result:
            raise ValidationError('An account using the same Email already exists.Please select a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if session["name"]!=username.data:
            cursor.execute(''' SELECT user_name from User_Profile 
                                            where user_name=%s''', [username.data])
            result = cursor.fetchone()
            if result:
                raise ValidationError('This Username already exists.Please select a different one')

    def validate_email(self, email):
        if session["email"]!=email.data:
            cursor.execute(''' SELECT user_email from User_Profile 
                                            where user_email=%s''', [email.data])
            result = cursor.fetchone()
            if result:
                raise ValidationError('An account using the same Email already exists.Please select a different one')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        cursor.execute(''' SELECT user_email from User_Profile 
                                            where user_email=%s''', [email.data])
        result = cursor.fetchone()
        if result is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    tags = StringField('Tags',validators=[DataRequired()])
    submit = SubmitField('Post')