from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__) #creates the flask application

app.config.from_object(Config) #flask looks inside the Config class in config.py and copies all uppercae variables into app.config (flasks config system) load confiiguration settings

db = SQLAlchemy(app) #db becomes your ORM interface, this line intilize the SQLAlchemy extension and connects it to Flask app, like plugging the database engine
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login' #type:ignore

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost= (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),fromaddr='no-reply@' + app.config['MAIL_SERVER'], toaddrs=app.config['ADMINS'], subject='Microblog Faliure', credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

from app import routes, models, errors #models define the structure of the database

