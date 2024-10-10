from flask import Flask
from flask_bcrypt import Bcrypt

api_link = "http://127.0.0.1:8000"
app = Flask(__name__)
bcrypt = Bcrypt(app)

from blogwebsite import routes
