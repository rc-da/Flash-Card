from flask import Blueprint, request, jsonify, session
from model.user_model import User_Profile
import requests

user_bp = Blueprint('user', __name__)

# Create
@user_bp.route("/signup", methods = ["POST"])
def signup():

    data = request.get_json()
    if all(key in data for key in ["user_name", "user_mail", "password"]):

        signup_response = User_Profile.create_user(
            data["user_name"],
            data["user_mail"],
            data["password"]
        )

        if signup_response["status"] == "success":
            
            return jsonify(signup_response), 200
        
        return jsonify(signup_response), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400


# Read
@user_bp.route("/login", methods = ["POST"])
def login():

    data = request.get_json()
    
    if "user_mail" in data and "password" in data:

        auth_response = User_Profile.authenticate_user(
            data["user_mail"],
            data["password"]
            )

        if auth_response["status"] == "success":
            session["user_id"] = auth_response["user_id"]
            session["user_name"] = auth_response["user_name"]
            session["user_mail"] = data["user_mail"]
            session.permanent = True

            print(auth_response, session.get("user_id"))
            return jsonify(auth_response), 200
        
        return jsonify(auth_response), 401
    
    return jsonify({
        "message" : "Missing required fields!" ,
        "status" : "failed"    
    }), 400

# Update
@user_bp.route("/logout", methods = ["POST"])
def logout():
    session.clear()

    return jsonify({
        "message" : "Logged out successfully!",
        "status" : "success"
    }), 200


# Delete
@user_bp.route("/delete", methods = ["DELETE"])
def delete_user():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    user_mail = session.get("user_mail")
    
    progress_response = requests.delete("http://127.0.0.0:5000/progress/delete/all")
    if progress_response["status"] == "failed":
        return jsonify({
            "message" : "Deletion of progress failed",
            "status" : "failed"
        }), 401
    
    card_response = requests.delete("http://127.0.0.0:5000/card/delete/all")

    if card_response["status"] == "failed":
        return jsonify({
            "message" : "Deletion of card failed",
            "status" : "failed"
        }), 401

    delete_response = User_Profile.delete_user(user_mail)
    
    if delete_response["status"] == "success":
        return jsonify(delete_response), 200
    
    return jsonify(delete_response), 401

# Update
@user_bp.route("/update", methods = ["PUT"])
def update_user():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    data = request.get_json()
    if all(key in data for key in ["user_name", "user_mail", "password"]):

        update_response = User_Profile.update_user(
            user_id, 
            data["user_name"], 
            data["user_mail"],
            data["password"]
            )
        
        if update_response["status"]:
            return jsonify(update_response), 200
        
        return jsonify(update_response), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400

    
@user_bp.route("/session")
def give_session():
    print(session)
    return jsonify({
       "user_id": session.get("user_id"),
        "user_mail" :session.get("user_mail")
    }), 200

@user_bp.route("/fetch")
def fetch_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = User_Profile.get_user(user_id)
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401
    

