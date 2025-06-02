from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import pdfplumber

load_dotenv(r"C:\Users\rohan.rf\PycharmProjects\PythonProject\key.env")

client = AzureOpenAI(
    api_key=os.getenv("api_key"),
    api_version="",
    azure_endpoint=os.getenv("azure_endpoint")
)


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()


pdf_path = r"C:\Users\rohan.rf\PycharmProjects\PythonProject\resume.pdf"
resume = extract_text_from_pdf(pdf_path)

with open(r'C:\Users\rohan.rf\PycharmProjects\PythonProject\jd.txt', 'r') as file:
    job_description = file.read()

question_prompt = f"""
You are an expert technical interviewer specializing in uncovering candidates' true depth of knowledge. Generate 6-8 interview questions that reveal:

1. Mandatory JD-aligned skills
2. Hidden strengths beyond JD requirements 
3. Conceptual mastery and problem-solving approach

Inputs:
- Job Description: {job_description}
- Candidate Resume: {resume}

Question Requirements:
1. JD-Specific :
   - Validate core required skills
   - Include practical implementation details
   - Example: "The JD requires [X]. How would you implement this to handle [specific challenge]?"

2. Beyond-JD:
   - Explore resume items not mentioned in JD
   - Probe advanced/niche expertise
   - Example: "Your resume shows [Y]. How would this apply to [novel scenario]?"

3. Stress-Test :
   - Challenge their knowledge boundaries
   - Ask for improvements to standard tools/processes
   - Example: "How would you redesign [common tool] to solve [its limitation]?"

4. Meta-Skills :
   - Reveal learning and problem-solving approaches
   - Example: "Walk me through how you mastered [complex concept]"

Please generate thoughtful and varied questions upto 15 .
"""

question_response = client.chat.completions.create(
    model="synapt-dev-gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful technical interviewer."},
        {"role": "user", "content": question_prompt}
    ],
    temperature=0.7,
    max_tokens=800
)

questions = question_response.choices[0].message.content
print("Generated Interview Questions:\n", questions)
