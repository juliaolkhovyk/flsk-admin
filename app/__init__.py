from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.helpers import get_debug_flag
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from app.config import DevConfig, ProdConfig


app = Flask(__name__)

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app.config.from_object(CONFIG)

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)
csrf = CSRFProtect(app)
csrf.init_app(app)
login = LoginManager(app)
login.login_view = 'admin.login'

from app.models import User, Group, Applicant
from app.admin import admin
