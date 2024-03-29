########################################################################
#################        Importing packages      #######################
########################################################################
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from utils.config import cfg
import sqlite3, os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
    app.config['SECRET_KEY'] = 'secret-key-goes-here' # it is used by Flask and extensions to keep data safe
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=cfg.PROCESS.LIFE_TIME)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #it is the path where the SQLite database file will be saved
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # deactivate Flask-SQLAlchemy track modifications
    try:
        db.init_app(app) # Initialiaze sqlite database
        print("SQLite Success")
    except Exception as e:
        print("SQLite ERROR", e)
    # The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login
    from utils.models import User
    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    from utils.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app