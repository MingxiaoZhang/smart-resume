from flask import Blueprint, request, jsonify
from src.models import User, Experience, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

experience = Blueprint('experience', __name__)

@experience.route('/add_experience', methods=['POST'])
@jwt_required()
def add_experience():
    current_user = get_jwt_identity()
    data = request.get_json()
    company = data['company']
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') if 'end_date' in data else None
    job_title = data['job_title']
    accomplishments = data['accomplishments']
    
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

@experience.route('/get_experiences', methods=['GET'])
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
