from openai import OpenAI

client = OpenAI()

def generate_markdown_resume(job_description, applicant_experience):
    prompt = f"""
    Job Description:
    {job_description}
    
    Applicant Experience:
    {applicant_experience}
    
    Create a resume in Markdown format that highlights the most relevant experience for the job description. Use the following structure:
    
    ## Summary
    - [Your professional summary here]
    
    ## Key Skills
    - Skill 1
    - Skill 2
    - Skill 3
    
    ## Relevant Experience
    - Experience 1
    - Experience 2
    - Experience 3
    """
    
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=256,
    )
    
    return response.choices[0].text.strip()

job_description = """
We are looking for a software engineer with 5+ years of experience in Python, Django, and REST APIs. The candidate should have a strong understanding of database management and cloud services (AWS, Azure).
"""

applicant_experience = """
- Developed several REST APIs using Python and Django.
- Managed cloud-based applications and databases on AWS and Azure.
- Led a team of 5 software engineers.
- Implemented CI/CD pipelines using Jenkins and Docker.
- Extensive experience in front-end technologies including React and Angular.
- Participated in code reviews and provided mentorship to junior developers.
"""

markdown_resume = generate_markdown_resume(job_description, applicant_experience)
print("Generated Resume in Markdown:\n", markdown_resume)
