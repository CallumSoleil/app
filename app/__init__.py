from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='/login'
login_manager.login_message="Login or register a new account"
app.secret_key=b'49f0d9ba4a0a075b63845231ba20d3445d916901cd4b498406503ca8e32aca25'

from app import views, models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))