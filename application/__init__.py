# import Flask class from the flask module
from flask import Flask
# import SQLAlchamy class from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#import os Module
from os import getenv
#import bcrypt
from flask_bcrypt import Bcrypt
#import from flask_login
from flask_login import LoginManager
# create a new instance of Flask and store it in app 
app = Flask(__name__)
#add bcrypt object
bcrypt = Bcrypt(app)
#add loginmanager object
login_manager = LoginManager(app)
#defining which function handles logins
login_manager.login_view = 'login'
#add the URI to the app
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI2')
# set this to avoid getting warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY2')

# create the database object
db=SQLAlchemy(app)

# import the ./application/routes.py file
from application import routes