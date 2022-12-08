from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from server.model import *

profile_controler = Blueprint("profile_controler", __name__)

# @profile_controler.route("api/profile/<int:user_id>/<string:user_name>/<string:email>", methods = ["GET","POST"])
# def lookup_profile(user_id,user_name,email):
#     try:
#         profile_data = User(username = user_name, user_id = user_id, email= email)
#         return