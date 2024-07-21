from flask import Blueprint, request, jsonify
from src.models import User, Experience, Resume, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.rag import get_resume

resume = Blueprint('resume', __name__)

@resume.route('/generate_resume', methods=['POST'])
@jwt_required()
def generate_resume():
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
    experiences = Experience.query.filter_by(user_id=user.id).all()
    data = request.get_json()
    company = data.get('company')
    job_title = data.get('title')
    job_description = data.get('description')
    job_data = {"company": company, "title": job_title, "description": job_description}
    resume = get_resume(user_info=user_info, experiences=experiences, job_data=job_data)

    new_resume = Resume(
        user_id=user.id,
        company=company,
        job_title=job_title,
        job_description=job_description,
        creation_date=datetime.now(),
        last_edit_date=datetime.now(),
        resume=resume
    )
    
    db.session.add(new_resume)
    db.session.commit()
    
    return jsonify({'resumeId': new_resume.id}), 201

@resume.route('/get_resume', methods=['GET'])
@jwt_required()
def get_resume_by_id():
    id = request.args.get('resumeId')
    resume = Resume.query.get(id)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
   
    return jsonify({'resume': resume.resume}), 200

@resume.route('/get_all_resume', methods=['GET'])
@jwt_required()
def get_all_resume():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    resumes = Resume.query.filter_by(user_id=user.id).all()
    
    resume_list = [{
        'company': resume.company,
        'creation_date': resume.creation_date.strftime('%Y-%m-%d'),
        'last_edit_date': resume.end_date.strftime('%Y-%m-%d'),
        'job_title': resume.job_title,
        'job_description': resume.job_description,
        'resume': resume.resume
    } for resume in resumes]
    
    return jsonify({'resumeList': resume_list}), 200

@resume.route('/update_resume', methods=['PUT'])
@jwt_required()
def update_resume():
    data = request.get_json()
    resume_id = data.get('resumeId')
    resume_text = data.get('resumeText')
    
    resume = Resume.query.get(resume_id)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
    
    resume.resume = resume_text
    
    db.session.commit()
    
    return jsonify({'message': 'Resume updated successfully!'}), 200