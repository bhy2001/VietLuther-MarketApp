import os
from time import strftime
from flask import Flask, render_template, session, redirect, url_for, request
from flask_cors import CORS, cross_origin
from .db.db import init_SQLAlchemy
from .utils import hash_pw
from .db.db import DB as db


app = Flask(__name__)
CORS(app=app, origins=["http://localhost:3000"])


# Register blueprint
from . import userSignin, userSignup, request_controler, profile_controler
app.register_blueprint(userSignin.user_sign_in)
app.register_blueprint(userSignup.user_sign_up)
app.register_blueprint(request_controler.request_controler)
app.register_blueprint(profile_controler.profile_controler)
