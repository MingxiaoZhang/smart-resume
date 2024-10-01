from flask import Blueprint, request, jsonify
from src.models import db, bcrypt, User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    response = jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

    return response, 200

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        username=email,
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)

    response = jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })
    
    return response, 201

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return jsonify(access_token=new_access_token), 200
    except:
        return jsonify({"msg": "Unable to refresh"}), 401