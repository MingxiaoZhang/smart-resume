import enum
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class AccountType(enum.Enum):
    ADMIN = "admin"
    PREMIUM = "premium"
    FREE = "free"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    city = db.Column(db.String(50))
    address = db.Column(db.String(150))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    skills = db.Column(db.ARRAY(db.String(50)), nullable=True)
    years_of_experience = db.Column(db.Integer)
    metadata = db.relationship('UserMetadata', uselist=False, back_populates='user')
    web_accounts = db.relationship("WebAccount", back_populates="user")
    experiences = db.relationship('Experience', backref='user', lazy=True)
    education = db.relationship('Education', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    resumes = db.relationship('Resume', backref='user', lazy=True)

class UserMetadata(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    profile_picture = db.Column(db.String)
    creation_date = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    premium_date = db.Column(db.DateTime)
    is_email_verified = db.Column(db.Boolean)
    is_email_subscribed = db.Column(db.Boolean)
    preferences = db.Column(db.JSON)
    user = db.relationship("User", back_populates="metadata")

class WebAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    user = db.relationship("User", back_populates="WebAccount")

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    job_title = db.Column(db.String(150), nullable=False)
    accomplishments = db.Column(db.Text, nullable=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    resume = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    last_edit_date = db.Column(db.Date, nullable=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    school = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(150), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    courses_taken = db.Column(db.Text, nullable=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_org = db.Column(db.String(150), nullable=True)
    project_name = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    project_link = db.Column(db.String(150), nullable=True)
    accomplishments = db.Column(db.Text, nullable=True)