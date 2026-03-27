import jwt
import bcrypt
from datetime import datetime, timedelta , timezone
from dotenv import load_dotenv
import os
from functools import wraps
from flask import request, jsonify

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  
    
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401
        
        token = auth_header.replace("Bearer ", "")
        try:
            payload = decode_token(token)
            request.user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return wrapper
#     # Test password hashing
#     hashed = hash_password("mypassword123")
#     print("Hashed:", hashed)
#     print("Match:", check_password("mypassword123", hashed))
#     print("Wrong:", check_password("wrongpassword", hashed))

#     # Test token
#     token = generate_token(user_id=1)
#     print("Token:", token)
#     print("Decoded:", decode_token(token))
