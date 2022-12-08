#!/usr/bin/env python3
import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
from config import app, db
from models import User,item, BuyRequest
from utils import hash_pw, check_pw


app = Flask(__name__)
CORS(app=app)

## sign in 
@app.route("/api/signin", methods=["POST"])
@cross_origin()
def api_user_signin():
    try:
        params = request.get_json(force=True)
        username = params.get("username", "")
        user_password_input = params.get("password", "")

        if username == "" or user_password_input == "":
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

        # Connect and fetch data from the users table
        user_data = User.select(username)

        # User not found
        if not user_data:
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

        user_password_hash = user_data.password_hash

        if check_pw(user_password_input, user_password_hash):
            session["user"] = (user_data.id, username)
            payload = {
                "status": "Successful",
                "sessionCookie": "",
                "currentUserID": user_data.id
            }
            return jsonify(payload), 200
        else:
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

    except Exception as error:
        return jsonify({"error": "Bad request. " + str(error)}), 404

#sign up
@app.route("/api/signup", methods=["POST"])
@cross_origin()
def api_user_signup():
    try:
        params = request.form
        username = params.get("username", "")
        student_id = params.get("student_id", "")
        email = params.get("email", "")
        phone_number = params.get("phone_number", "")
        password = params.get("password", "")
        confirmPassword = params.get("confirmPassword", "")


        # Verify password
        if password != confirmPassword:
            session["error"] = "Password does not match. Please try again."
            raise Exception(session["error"])

        # Verify username
        user_data = User.select(username)
        if user_data is not None:
            # Username taken
            session["error"] = "Username has been taken. Please try a different username."
            raise Exception(session["error"])
        else:
            # Hash the password
            password_hash = hash_pw(password)
            new_user = User(username=username,student_id = student_id, email=email,phone_number =phone_number, password_hash=password_hash)

            # Add user to the database
            User.insert(new_user)

            # Create a session for this user
            session["user"] = (new_user.id, username)
            payload = {
                "status": "Successful",
                "sessionCookie": "",
                "currentUserID": new_user.id
            }
            return jsonify(payload), 200

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400

# request controler
@app.route("/api/request/all", methods=["GET","POST"])
@cross_origin()
def get_all_available_request():
    try:
        all_request_data = BuyRequest.get_all_requests(request_status="available")
        if not all_request_data:
            raise Exception("No request found")
        return jsonify(all_request_data), 200

    except Exception as error:
        return jsonify({"error": "Bad request. " + str(error)}), 404

@app.route("api/request/add/<int:initiator_id>/<int:request_time>/<int:price>", methods = ["GET","POST"])
@cross_origin()
def add_new_request(initiator_id,request_time,price):
    try:
        new_request = BuyRequest(
            initiator_id = initiator_id, 
            request_time= request_time, 
            price= price)
        
        BuyRequest.insert(new_request=new_request)

        request_id = new_request.id
        items = request.get_json(force =True)
        if not items:
            raise Exception ("bad Json")
        for i in items:
            new_item = item(request_id=request_id,item_name= i, item_quanity = items.i)
            item.insert(new_item==new_item)
        return "Success",200
    except Exception as error:
        return jsonify({"error": "Bad request. " + str(error)}), 404

@app.route("api/request/remove/<int:request_id>", methods = ["POST"])
@cross_origin()
def remove_request(request_id:int):
    try:
        request_data = BuyRequest.get_request_by_request_id(request_id=request_id)
        if not request_data:
            raise Exception("No request found")

        BuyRequest.delete(request_data=request_data.id)
        item.delete_request_id(request_id=request_data.id)
        return "Success", 200

    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@app.route("api/request/accept/<int:request_id>/<int:accepter_id>/<int:accepted_time>", methods = ["POST"])
@cross_origin()
def accpet_request(request_id:int,accepter_id:int,accepted_time:int):
    try:
        request_data = BuyRequest.get_request_by_request_id(request_id=request_id)
        if not request_data:
            raise Exception("No request found")
        BuyRequest.accept_request(request_id=request_id,receiver_id=accepter_id,time=accepted_time)
        return "Success", 200

    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400