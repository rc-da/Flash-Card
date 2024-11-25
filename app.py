from flask import Flask, session, jsonify
from flask_cors import CORS
from controller.user_controller import user_bp
from controller.progress_controller import progress_bp
from controller.category_controller import category_bp
from controller.card_controller import card_bp

app = Flask(__name__)

app.secret_key = "hji"

app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  
    SESSION_COOKIE_PATH='/',
    SESSION_PERMANENT=False,
)

CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(card_bp, url_prefix="/card")
app.register_blueprint(progress_bp, url_prefix="/progress")
app.register_blueprint(category_bp, url_prefix="/category")

if __name__ == "__main__":
    app.run(debug=True)  
