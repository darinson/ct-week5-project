from flask import Flask
from config import Config

from .site.routes import site
from .authentication.routes import auth

from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma

from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

ma.init_app(app)

CORS(app)

from marvel_collection import models