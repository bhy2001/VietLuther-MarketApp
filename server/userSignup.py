from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from server.utils import hash_pw
from server.model import User

user_sign_up = Blueprint("user_sign_up", __name__)

@user_sign_up.route("/signup", methods=["GET"])
def user_signup():
    return render_template("user_signup.html")

@user_sign_up.route("/api/signup", methods=["POST"])
def api_user_signup():
    try:
        params = request.form
        username = params.get("username", "")
        password = params.get("password", "")
        confirmPassword = params.get("confirmPassword", "")
        email = params.get("email", "")

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
            new_user = User(username=username, email=email, password_hash=password_hash)

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
