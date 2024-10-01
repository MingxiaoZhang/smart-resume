from flask import Blueprint, request, jsonify
from src.models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

user = Blueprint('user', __name__)

@user.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    print(request)
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({'user': user.username}), 200

@user.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user_info = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    
    return jsonify({'user_info': user_info}), 200

@user.route('/update_info', methods=['PUT'])
@jwt_required()
def update_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    
    db.session.commit()
    
    return jsonify({'message': 'User information updated successfully!'}), 200

