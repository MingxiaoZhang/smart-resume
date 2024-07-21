from datetime import datetime
from flask import Blueprint, request, jsonify
from src.models import User, Education, db
from flask_jwt_extended import jwt_required, get_jwt_identity

education = Blueprint('education', __name__)

@education.route('/get_education', methods=['GET'])
@jwt_required()
def get_education():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    education = Education.query.filter_by(user_id=user.id).all()
    
    education_list = [{
        'id': edu.id,
        'school': edu.school,
        'degree': edu.degree,
        'start_date': edu.start_date.strftime('%Y-%m-%d'),
        'end_date': edu.end_date.strftime('%Y-%m-%d') if edu.end_date else None,
        'courses_taken': edu.courses_taken
    } for edu in education]
    
    return jsonify({'education': education_list}), 200

@education.route('/add_education', methods=['POST'])
@jwt_required()
def add_education():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    school = data.get('school')
    degree = data.get('degree')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if 'end_date' in data else None
    courses_taken = data.get('courses_taken')

    new_education = Education(
        user_id=user.id,
        school=school,
        degree=degree,
        start_date=start_date,
        end_date=end_date,
        courses_taken=courses_taken
    )
    
    db.session.add(new_education)
    db.session.commit()
    
    return jsonify({'message': 'Education added successfully!'}), 201

@education.route('/update_education', methods=['PUT'])
@jwt_required()
def update_info():
    data = request.get_json()
    id = data.get('id')
    school = data.get('school')
    degree = data.get('degree')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if 'end_date' in data else None
    courses_taken = data.get('courses_taken')
    
    education = Education.query.get(id)
    
    education.school = school
    education.degree = degree
    education.start_date = start_date
    education.end_date = end_date
    education.courses_taken = courses_taken 
    
    db.session.commit()
    
    return jsonify({'message': 'Education updated successfully!'}), 200