from flask import Blueprint, request, jsonify, session
from model.progress_model import Progress

progress_bp = Blueprint("progress", __name__)

@progress_bp.route("/<int:id>")
def get_progress(id):
    if "user_id" not in session:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    
    response = Progress.get_progress(id)

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

@progress_bp.route("/delete/all", methods = ["DELETE"])
def delete_all_progress():
    user_id = session.get("user_id")
    if user_id:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    
    response = Progress.delete_all_progress(user_id)
    
    return response

@progress_bp.route("/delete/<int:card_id>", methods = ["DELETE"])
def delete_progress(card_id):
    response = Progress.delete_progress(card_id)

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

@progress_bp.route("/reminder/<int:card_id>")
def get_reminder(card_id):
    if "user_id" not in session:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    
    response = Progress.get_reminder(card_id)

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

@progress_bp.route("/update", methods=["PUT"])
def update_rating():
    if "user_id" not in session:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    data = request.get_json()
    if all(key in data for key in ["card_id", "rating", "reminder"]):
        response = Progress.update_progress(
            data["card_id"],
            data["rating"],
            data["reminder"]
        )

        if response["status"] == "success":
            return jsonify(response), 200
        
        return jsonify(response), 401
    
    return jsonify({
        "status" : "failed",
        "message" : "Missing required fields!"
    }), 400

@progress_bp.route("/create", methods=["POST"])
def create_progress():
    user_id = session.get("user_id")
    if user_id:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    data = request.get_json()
    if "card_id" in data:
        response = Progress.create_progress(data["card_id"], user_id)

        if response["status"] == "success":
            return jsonify(response), 200
        
        return jsonify(response), 401
    
    return jsonify({
        "status" : "failed",
        "message" : "Missing required fields!"
    }), 400