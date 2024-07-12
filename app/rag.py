import os
from dotenv import load_dotenv
import cohere

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=api_key)

def build_title(experience):
    return f"{experience.job_title} at {experience.company}"

def build_snippet(experience):
    snippet = f"{experience.job_title} at {experience.company} from {experience.start_date.strftime('%Y-%m-%d')} to {experience.end_date.strftime('%Y-%m-%d')}. \n"
    for accomplishment in experience.accomplishments:
        snippet += f"{accomplishment}\n"
    print(snippet)
    return snippet

def build_documents_for_rag(experiences):
    return [{"title": build_title(exp), "snippet": build_snippet(exp)} for exp in experiences]

def get_resume(experiences):
    documents = build_documents_for_rag(experiences)
    res = co.chat(
        model="command-r-plus",
        message="Generate a resume based on the following experiences:\n\n",
        documents=documents
    )
    return res.text