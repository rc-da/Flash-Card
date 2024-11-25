from flask import Blueprint, request, jsonify, session
from model.category_model import Category

category_bp = Blueprint("category", __name__)

@category_bp.route("/all")
def get_all_category():
    if "user_id" not in session:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    
    response = Category.fetch_all_category()

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401

@category_bp.route("/<int:id>")
def get_category(id):
    if "user_id" not in session:
        return {
            "message" : "User not Authorized",
            "status" : "failed"
        }
    
    response = Category.fetch_category(id)

    if response["status"] == "success":
        return jsonify(response), 200
    
    return jsonify(response), 401