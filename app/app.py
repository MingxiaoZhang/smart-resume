from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, Experience
from datetime import datetime
from rag import get_resume

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/update_info', methods=['PUT'])
@jwt_required()
def update_info():
    current_user = get_jwt_identity()
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    user = User.query.filter_by(username=current_user).first()
    
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

@app.route('/add_experience', methods=['POST'])
@jwt_required()
def add_experience():
    current_user = get_jwt_identity()
    data = request.get_json()
    company = data['company']
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') if 'end_date' in data else None
    job_title = data['job_title']
    accomplishments = data.get('accomplishments', [])
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    new_experience = Experience(
        user_id=user.id,
        company=company,
        start_date=start_date,
        end_date=end_date,
        job_title=job_title,
        accomplishments=accomplishments
    )
    
    db.session.add(new_experience)
    db.session.commit()
    
    return jsonify({'message': 'Experience added successfully!'}), 201

@app.route('/get_experiences', methods=['GET'])
@jwt_required()
def get_experiences():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    experiences = Experience.query.filter_by(user_id=user.id).all()
    
    experiences_list = [{
        'company': exp.company,
        'start_date': exp.start_date.strftime('%Y-%m-%d'),
        'end_date': exp.end_date.strftime('%Y-%m-%d') if exp.end_date else None,
        'job_title': exp.job_title,
        'accomplishments': exp.accomplishments
    } for exp in experiences]
    
    return jsonify({'experiences': experiences_list}), 200

@app.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user_info = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    
    return jsonify({'user_info': user_info}), 200

@app.route('/get_resume', methods=['GET'])
@jwt_required()
def generate_resume():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    experiences = Experience.query.filter_by(user_id=user.id).all()
    
    resume = get_resume(experiences=experiences)
    
    return jsonify({'resume': resume}), 200

if __name__ == '__main__':
    app.run(debug=True)
