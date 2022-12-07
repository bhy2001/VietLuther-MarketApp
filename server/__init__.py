import os
from time import strftime
from flask import Flask, render_template, session, redirect, url_for, request
from flask_cors import CORS
from .db.db import init_SQLAlchemy
from .utils import hash_pw
from .db.db import DB as db