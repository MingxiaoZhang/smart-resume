from flask import request, jsonify, current_app as app
import cohere
import os

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    data = request.get_json()
    experiences = data.get('experiences', [])
    prompt = "Generate a resume based on the following experiences:\n\n"

    for experience in experiences:
        prompt += f"- {experience}\n"

    prompt += "\nResume:\n"

    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key=api_key)
    response = co.chat(
        model="command-r-plus",
        message=prompt
    )

    return jsonify(response.text)
