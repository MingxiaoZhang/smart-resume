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

def build_documents_for_rag(experiences, job_description):
    documents = [{"title": build_title(exp), "snippet": build_snippet(exp)} for exp in experiences]
    documents.append({"title": "Job Description", "snippet": job_description["text"]})

def get_resume(experiences, job_description):
    documents = build_documents_for_rag(experiences=experiences, job_description=job_description)
    res = co.chat(
        model="command-r-plus",
        message=f"Generate a resume for the job of {job_description['title']} at {job_description['company']} based on the following job description and candidate's work experiences:\n",
        documents=documents
    )

    return res.text