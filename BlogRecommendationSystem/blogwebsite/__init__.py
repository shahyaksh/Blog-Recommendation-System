import time
import os
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import Flask, session
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import smtplib

app = Flask(__name__)
mysql = MySQL()
bcrypt = Bcrypt(app)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Yaksh_170802'
app.config['MYSQL_DATABASE_DB'] = 'blog_recommendation_system'
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")


while True:
    try:
        mysql.init_app(app)
        break
    except Exception as error:
        print("Connection to Database failed")
        print(error)
        time.sleep(2)

conn = mysql.connect()
cursor = conn.cursor()
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
        cursor.execute(''' select * from user_profile where user_id=%s ''', (user_id,))
        user_details = cursor.fetchone()
        return user_details


from blogwebsite import routes
