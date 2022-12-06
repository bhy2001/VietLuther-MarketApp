import sqlite3
import os
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

# Create an SQLAlchemy instance that is used throughout the application. As we create a Flask instance
# dynamically by using factory pattern, we cannot pass it here (DB = SQLAlchemy(app)) because the app
# instance has not existed. Inside the factory function to create a Flask app instance, we need to call
# init_SQLAlchemy function which in turns will call DB.init_app(current_app) to initialize the use of
# the app with this database setup and call DB.create_all() to create the tables.
DB = SQLAlchemy()

# Initialize the database
def init_SQLAlchemy() -> None:
    # Explicitly register tables' information
    from server.model import User, BuyRequest, item

    DB.init_app(current_app)
    DB.create_all()