#!/usr/bin/env python3
import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from config import app, db
from models import User,item, BuyRequest, ItemSchema, BuyRequestschema
from utils import hash_pw, check_pw
from flask_cors import CORS, cross_origin

## sign in 
@app.route("/api/signin/<string:username>/<string:password>", methods=["GET","POST"])
@cross_origin()
def api_user_signin(username:str, password:str):
    if not username and not password:
        err = "Invalid login credentials. Please try again."
    # Connect and fetch data from the users table
    user_data = User.select(username)
    # User not found
    if not user_data:
        err = "Invalid login credentials. Please try again."

    user_password_hash = user_data[0].password_hash

    if check_pw(password, user_password_hash):
        payload = {
            "status": "Successful",
            "sessionCookie": "",
            "currentUserID": user_data[0].id,
            "currentUserName": user_data[0].username
        }
        return jsonify(payload), 200
    else:
        err = "Invalid login credentials. Please try again."
    return jsonify(err)

#logout
@app.route('/api/logout', methods=["GET","POST"])
@cross_origin()
def api_user_logout():
    return "Successfull log out"

#sign up
@app.route(
    "/api/signup/<string:username>/<int:student_id>/<string:email>/<int:phone_number>/<string:password>/<string:confirmPassword>",
    methods=["GET","POST"])
@cross_origin()
def api_user_signup(
    username: str,student_id: int, email: str,
    phone_number: int, password: str, confirmPassword:str
):
    # Verify password
    if password != confirmPassword:
        err = "Password does not match. Please try again."
        return jsonify(err)

    # Verify username
    user_data = User.select(username)
    if user_data is not None:
        # Username taken
        err = "Username has been taken. Please try a different username."
        return jsonify(err)
        
    else:
        # Hash the password
        password_hash = hash_pw(password)
        new_user = User(username=username,student_id = student_id, email=email,phone_number =phone_number, password_hash=password_hash)
        # Add user to the database
        User.insert(new_user)

        # Create a session for this user
        # session["user"] = (new_user.id, username)
        payload = {
            "status": "Successful",
            "sessionCookie": "",
            "currentUserID": new_user[0].id,
            "currentUserName": new_user[1].username
        }
        return jsonify(payload), 200

# request controler
# @app.route("/api/request/all", methods=["GET","POST"])
# 
# def get_all_available_request():
#     try:
#         all_request_data = BuyRequest.get_all_requests(request_status="available")
#         if not all_request_data:
#             raise Exception("No request found")
#         return jsonify(all_request_data), 200

#     except Exception as error:
#         return jsonify({"error": "Bad request. " + str(error)}), 404
# show your accepted request
@app.route("/api/request/all", methods=["GET","POST"])
@cross_origin()
def get_all_available_request():
    request = BuyRequest.query.filter(BuyRequest.request_status == "available")    
    
    request_schema = BuyRequestschema(many=True)
    all_request_data = request_schema.dump(request)
    if not all_request_data:
        return "No request found"
    else:
        all_data = []
        for i in all_request_data:
            print (i)
            items = item.query.filter(item.request_id == i["id"])  
            item_schema = ItemSchema( many = True)
            request_items = item_schema.dump(items)
            all_data.append([i,request_items])

        return jsonify(all_data), 200


# add new Request
@app.route("/api/request/add/<int:initiator_id>/<int:request_time>/<int:price>", methods = ["GET","POST"])
@cross_origin()
def add_new_request(initiator_id,request_time,price):
    try:
        new_request = BuyRequest(
            initiator_id = initiator_id, 
            request_time= request_time, 
            price= price)
        if request.method == "POST":
            items = request.get_json(force =True)
        print (initiator_id, request_time, price)
        print(items)
        BuyRequest.insert(new_request=new_request)

        request_id = new_request.id
        # items = request.get_json(force =True)
        # print(items)
        if not items:
            raise Exception ("bad Json")
        for i in items.body:
            new_item = item(request_id=request_id,item_name= i, item_quanity = items.i)
            item.insert(new_item=new_item)
        payload = {
                "status": "Successful",
                "sessionCookie": "",
                "curentRequestId": new_request.id
            }
        return jsonify(payload), 200
    except Exception as error:
        return jsonify({"error": "Bad request. " + str(error)}), 404

@app.route("/api/request/remove/<int:request_id>", methods = ["GET","POST"])
@cross_origin()
def remove_request(request_id:int):
    try:
        BuyRequest.delete_by_condition(request_id=request_id)
        item.delete_request_id(request_id=request_id)
        # BuyRequest.query.filter(BuyRequest.id == request_id).delete(synchronize_session=False)
        # item.query.filter(item.request_id == request_id).delete(synchronize_session=False)
        return "Success", 200
    except:
        return "not found request"


@app.route("/api/request/accept/<int:request_id>/<int:accepter_id>/<int:accepted_time>", methods = ["GET","POST"])
@cross_origin()
def accept_request(request_id:int,accepter_id:int,accepted_time:int):
    try:    
        request_data = BuyRequest.get_request_by_request_id(request_id=request_id)
        if not request_data:
            return jsonify({"Error":"No request found"})
        BuyRequest.accept_request(request_id=request_id,receiver_id=accepter_id,time=accepted_time)
        return "Success", 200
    except:
        return "Error"
