from flask import Blueprint, request, jsonify
import logging
import jwt
from datetime import datetime, timedelta
from config import Config

auth_bp = Blueprint('auth_bp', __name__)

USERNAME = "test123"
PASSWORD = "password123"

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')


        if not username or not password:
            logging.warning(f"{datetime.now()} Empty fields")
            return jsonify({'message': 'Username and password'}), 400
        
        if username == USERNAME and password == PASSWORD:
            token = jwt.encode({
                'username': username,
                'exp': datetime.now() + timedelta(minutes=20)
            }, Config.SECRET_KEY, algorithm='HS256')
            logging.info(f"[LOGIN SUCCESS!] username {username}")
            return jsonify({'message': 'Login Successful',
                            'username': username,
                            'token': token
                            }), 200
        logging.warning(f"{datetime.now()} Invalid credentials for {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        logging.error(f"Login error : {e}")
        return jsonify({'message': str(e)}), 500