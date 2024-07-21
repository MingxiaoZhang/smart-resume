from datetime import datetime
from flask import Blueprint, request, jsonify
from src.models import User, Project, db
from flask_jwt_extended import jwt_required, get_jwt_identity

project = Blueprint('project', __name__)

@project.route('/get_projects', methods=['GET'])
@jwt_required()
def get_projects():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    projects = Project.query.filter_by(user_id=user.id).all()
    
    projects_list = [{
        'project_name': project.project_name,
        'project_org': project.project_org,
        'start_date': project.start_date.strftime('%Y-%m-%d'),
        'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
        'project_link': project.project_link,
        'accomplishments': project.accomplishments
    } for project in projects]
    
    return jsonify({'projects': projects_list}), 200

@project.route('/add_project', methods=['POST'])
@jwt_required()
def add_project():
    current_user = get_jwt_identity()

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    project_name = data['project_name']
    project_org = data['project_org']
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') if 'end_date' in data else None
    project_link = data['project_link']
    accomplishments = data['accomplishments']

    new_project = Project(
        user_id=user.id,
        project_name=project_name,
        project_org=project_org,
        start_date=start_date,
        end_date=end_date,
        project_link=project_link,
        accomplishments=accomplishments
    )
    
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'message': 'Project added successfully!'}), 201

@project.route('/update_project', methods=['PUT'])
@jwt_required()
def update_project():
    data = request.get_json()
    id = data.get('id')
    project_name = data.get('project_name')
    project_org = data.get('project_org')
    project_link = data.get('project_link')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if 'end_date' in data else None
    accomplishments = data.get('accomplishments')
    
    project = Project.query.get(id)
    
    project.project_name = project_name
    project.project_org = project_org
    project.project_link = project_link
    project.start_date = start_date
    project.end_date = end_date
    project.accomplishments = accomplishments 
    
    db.session.commit()
    
    return jsonify({'message': 'Project updated successfully!'}), 200