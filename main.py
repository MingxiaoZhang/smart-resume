import os
from dotenv import load_dotenv
import cohere

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=api_key)

res = co.chat(
  model="command-r-plus",
  message="Generate a resume based on the following experiences:\n\n",
  documents=[
    {
      "title": "Software Engineer",
      "snippet": "Software Engineer at ABC Corp from June 2015 to August 2020. Developed web applications using JavaScript, React, and Node.js."
    },
    {
      "title": "Product Manager",
      "snippet": "Project Manager at XYZ Ltd. from September 2020 to Present. Led a team of 10 in developing a project management tool."
    }
  ])

print(res)