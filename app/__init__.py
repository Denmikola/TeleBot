# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_less import lessc

app = Flask(__name__)
app.config.from_object(Config)

lessc(app)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."

from app import routes, models, errors

