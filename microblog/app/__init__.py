from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) #creates the flask application
app.config.from_object(Config) #flask looks inside the Config class in config.py and copies all uppercae variables into app.config (flasks config system) load confiiguration settings

db = SQLAlchemy(app) #db becomes your ORM interface, this line intilize the SQLAlchemy extension and connects it to Flask app, like plugging the database engine
migrate = Migrate(app, db)

from app import routes, models #models define the structure of the database
