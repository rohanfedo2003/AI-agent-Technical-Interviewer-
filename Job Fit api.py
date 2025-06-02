from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pdfplumber
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables
load_dotenv("key.env")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("api_key"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("azure_endpoint")
)

# Extract text from PDF
def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

@app.post("/generate-questions/")
async def generate_questions(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(resume_file.file)

        # Read job description text
        job_description = jd_file.file.read().decode("utf-8")

        # Construct prompt
        prompt = f"""
You are an expert technical interviewer specializing in uncovering candidates' true depth of knowledge. Generate 6-8 interview questions that reveal:

1. Mandatory JD-aligned skills
2. Hidden strengths beyond JD requirements 
3. Conceptual mastery and problem-solving approach

Inputs:
- Job Description: {job_description}
- Candidate Resume: {resume_text}

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

Please generate thoughtful and varied questions up to 15 Questions.
"""


        response = client.chat.completions.create(
            model="synapt-dev-gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        questions = response.choices[0].message.content
        return JSONResponse(content={"questions": questions})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {e}")
