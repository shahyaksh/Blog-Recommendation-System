import os
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import smtplib
import requests

api_link = "http://127.0.0.1:8000"
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")

mail = Mail(app)

class User_Token:

    def get_reset_token(user_id, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"])
        return s.dumps({'user_id': user_id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        user_details = requests.get(f"{api_link}/user/details/id/{user_id}").json()
        return user_details


from blogwebsite import routes
