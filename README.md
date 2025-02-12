# Smart Resume Flask API with PostgreSQL

This project is a simple Flask API for generating user resume based on the user's experiences and the job description. It also provides enpoints for user registration, login, and managing user information and experiences. It uses PostgreSQL as the database and JWT for authentication.

## Features

- User registration
- User login with JWT authentication
- Update user information
- Add user experiences
- Get user experiences
- Get user information
- Generate resume

## Prerequisites

- Python 3.8+
- PostgreSQL
- Cohere

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MingxiaoZhang/smart-resume.git
cd smart-resume
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

- Install PostgreSQL and create a new database and user.

```sql
CREATE ROLE yourusername WITH LOGIN PASSWORD 'yourpassword';
CREATE DATABASE yourdatabase OWNER yourusername;
GRANT ALL PRIVILEGES ON DATABASE yourdatabase TO yourusername;
```

### 5. Get Cohere API Key

- Follow instructions at https://dashboard.cohere.com/api-keys to get an API key for Cohere.

### 5. Update Configuration

Edit `.env` with your PostgreSQL credentials and Cohere API key.

```
POSTGRES_URI=postgresql://<yourusername>:<yourpassword>@localhost:5432/<yourdatabase>
COHERE_API_KEY=<your_api_key>
```

### 6. Initialize the Database

Run the script to create the necessary tables.

```bash
python create_tables.py
```

### 7. Run the Application

```bash
python app/app.py
```

## API Endpoints

### Register a User

**Endpoint:** `POST /register`

**Payload:**
```json
{
    "username": "dummyuser",
    "password": "dummypassword"
}
```

**Response:**
```json
{
    "message": "User registered successfully!"
}
```

### Login

**Endpoint:** `POST /login`

**Payload:**
```json
{
    "username": "dummyuser",
    "password": "dummypassword"
}
```

**Response:**
```json
{
    "access_token": "your_jwt_token"
}
```

### Update User Information

**Endpoint:** `PUT /update_info`

**Headers:**
```http
Authorization: Bearer your_jwt_token
```

**Payload:**
```json
{
    "email": "dummyuser@example.com",
    "first_name": "Dummy",
    "last_name": "User"
}
```

**Response:**
```json
{
    "message": "User information updated successfully!"
}
```

### Add Experience

**Endpoint:** `POST /add_experience`

**Headers:**
```http
Authorization: Bearer your_jwt_token
```

**Payload:**
```json
{
    "company": "Dummy Company",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01",
    "job_title": "Dummy Job Title",
    "accomplishments": ["Accomplishment 1", "Accomplishment 2"]
}
```

**Response:**
```json
{
    "message": "Experience added successfully!"
}
```

### Get Experiences

**Endpoint:** `GET /get_experiences`

**Headers:**
```http
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
    "experiences": [
        {
            "company": "Dummy Company",
            "start_date": "2023-01-01",
            "end_date": "2024-01-01",
            "job_title": "Dummy Job Title",
            "accomplishments": ["Accomplishment 1", "Accomplishment 2"]
        }
    ]
}
```

### Get User Information

**Endpoint:** `GET /get_user_info`

**Headers:**
```http
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
    "user_info": {
        "username": "dummyuser",
        "email": "dummyuser@example.com",
        "first_name": "Dummy",
        "last_name": "User"
    }
}
```

### Generate Resume

**Endpoint:** `GET /get_resume`

**Headers:**
```http
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
    "resume": "{your_resume}"
}
```