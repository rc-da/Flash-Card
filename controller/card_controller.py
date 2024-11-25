from flask import Blueprint, request, jsonify, session
from model.card_model import Card
import requests

card_bp = Blueprint('card', __name__)


@card_bp.route("/create", methods = ["POST"])
def create_card():
    user_id = session.get("user_id")
    if not user_id:
        return {
            "message" : "User not authorized!",
            "status" : "failed"
        }

    data = request.get_json()
    if all(key in data for key in ["category_id", "card_front", "card_back"]):

        response = Card.create_card(
            user_id,
            data["category_id"],
            data["card_front"],
            data["card_back"]
        )

        if response["status"] == "success":
            
            return jsonify(response), 200
        
        return jsonify(response), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400



# Delete
@card_bp.route("/delete/<int:id>", methods = ["DELETE"])
def delete_card(id):

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    progress_response = requests.delete(f"http://127.0.0.1:5000/progress/delete/{id}")
    progress_response = progress_response.json()
    if progress_response["status"] == "failed":
        return jsonify(progress_response), 401
    
    response = Card.delete_card(id)
    
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

# Update
@card_bp.route("/update/<int:id>", methods = ["PUT"])
def update_card(id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    data = request.get_json()
    if all(key in data for key in ["category_id", "card_front", "card_back"]):

        response = Card.update_card(
            data["category_id"],
            data["card_front"],
            data["card_back"],
            id
            )
        
        if response["status"]:
            return jsonify(response), 200
        
        return jsonify(response), 401
    
    return jsonify({
        "message" : "Missing required fields!",
        "status" : "failed"
    }), 400

@card_bp.route("/<int:id>", methods = ["GET"])
def get_card(id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = Card.get_card(id)
        
    if response["status"]:
        return jsonify(response), 200      
      
    return jsonify(response), 401

@card_bp.route("/delete/all", methods = ["DELETE"])
def delete_all_card():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = Card.delete_all_card(user_id)
    
    return response

@card_bp.route("/fetch/all", methods = ["GET"])
def fetch_all_card():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = Card.fetch_all_card(user_id)
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

@card_bp.route("/fetch/unread", methods = ["GET"])
def fetch_all_unread():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "message" : "User is not authenticated!",
            "status" : "failed"
        }), 401
    
    response = Card.fetch_all_unread(user_id)
    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401
