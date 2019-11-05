from flask import Flask
from config import Config
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)
# right side is the function that's called to login users
login.login_view = 'login'

from app import routes, models
=======

myApp = Flask(__name__)
myApp.config.from_object(Config)

from app import routes
>>>>>>> master
