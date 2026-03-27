from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import User, engine
from auth import hash_password, check_password, generate_token

auth_bp = Blueprint("auth", __name__)   

@auth_bp.route("/register", methods=["POST"])
def register():
    data =request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400   
    
    with Session(engine) as session:
        if session.query(User).filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 400
        
        new_user = User(
            email=data["email"],
            password=hash_password(data["password"])
        )
        session.add(new_user)
        session.commit()

        return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    with Session(engine) as session:
        user = session.query(User).filter_by(email=data["email"]).first()
        if not user or not check_password(data["password"], user.password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        token = generate_token(user.id)
        return jsonify({"token": token}), 200