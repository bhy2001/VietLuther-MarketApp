from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from server.model import *

app = Blueprint("app", __name__)


@app.route("/api/request", methods=["GET","POST"])
def get_all_available_request():
    try:
        all_request_data = BuyRequest.get_all_requests(request_status="available")
        if not all_request_data:
            raise Exception("No request found")
        return jsonify(all_request_data), 200

    except Exception as error:
        return jsonify({"error": "Bad request. " + str(error)}), 404

@app.route("api/request/add/<int:initiator_id>/<int:request_time>/<int:price>", methods = ["GET","POST"])
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

