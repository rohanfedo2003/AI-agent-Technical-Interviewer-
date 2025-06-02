from fastapi import FastAPI, UploadFile, File, Form
from openai import AzureOpenAI
import pdfplumber
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\rohan.rf\PycharmProjects\PythonProject\key.env")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("api_key"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("azure_endpoint")
)

app = FastAPI()

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

@app.post("/evaluate/")
async def evaluate_candidate(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...),
    questions: UploadFile = File(...),
    candidate_answers: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume)

    # Build evaluation prompt
    evaluation_prompt = f"""
    You are a technical evaluator tasked with assessing a candidate for a Hotel Manager position.
    Please evaluate the candidate based on the following inputs:
    1. The job description
    2. The candidate's resume
    3. Their responses to job-specific and behavioral interview questions
    ---
    **Evaluation Criteria**:
    - Relevance and completeness of answers
    - Depth of knowledge and conceptual clarity
    - Problem-solving and decision-making ability
    - Communication and articulation
    - Alignment with the job role and responsibilities
    ---
    **Job Description**:
    {jd}

    ---

    **Candidate Resume**:
    {resume_text}

    ---

    **Interview Questions**:
    {questions}

    ---

    **Candidate Answers**:
    {candidate_answers}

    ---
    **Instructions**:
    Provide:
    - A total score out of 100
    - A brief justification summarizing the candidate's strengths and areas for improvement
    """

    # Call Azure OpenAI
    response = client.chat.completions.create(
        model="synapt-dev-gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a technical evaluator."},
            {"role": "user", "content": evaluation_prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    return {"evaluation": response.choices[0].message.content}
