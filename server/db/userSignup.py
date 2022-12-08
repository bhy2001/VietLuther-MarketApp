from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from server.utils import hash_pw
from server.model import User

app = Blueprint("app", __name__)

# @app.route("/signup", methods=["GET"])
# def user_signup():
#     return render_template("user_signup.html")

@app.route("/api/request", methods=["POST"])
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
