import json
import os
from dotenv import load_dotenv
import cohere

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=api_key)

def build_title(experience):
    return f"Work Experience: {experience.job_title} at {experience.company}"

def build_snippet(experience):
    snippet = f"The candidate worked as a {experience.job_title} at {experience.company} from {experience.start_date.strftime('%Y-%m-%d')} to {experience.end_date.strftime('%Y-%m-%d')}. Their achievements in their work are as follows: \n"
    for accomplishment in experience.accomplishments:
        snippet += f"{accomplishment}\n"
    return snippet

def get_resume(user_info, experiences, job_data):
    documents = [{"title": build_title(exp), "snippet": build_snippet(exp)} for exp in experiences]
    documents.append({"title": "Job Description", "snippet": job_data["description"]})
    documents.append({"title": "Basic Candidate Information", "snippet": json.dumps(user_info)})
    res = co.chat(
        model="command-r-plus",
        message=f"Generate a resume for the job of {job_data['title']} at {job_data['company']} based on the following job description and candidate's work experiences:\n",
        documents=documents
    )
    return res.text