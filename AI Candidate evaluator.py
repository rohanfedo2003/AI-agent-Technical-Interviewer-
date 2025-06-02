from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import pdfplumber
load_dotenv(r"C:\Users\rohan.rf\PycharmProjects\PythonProject\key.env")

client = AzureOpenAI(
    api_key=os.getenv("api_key"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("azure_endpoint")
)
with open(r'C:\Users\rohan.rf\PycharmProjects\PythonProject\qns.txt', 'r') as file:
    questions = file.read()

with open(r'C:\Users\rohan.rf\PycharmProjects\PythonProject\jd.txt', 'r') as file:
    job_description = file.read()

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()
pdf_path = r"C:\Users\rohan.rf\PycharmProjects\PythonProject\resume.pdf"
resume_text=extract_text_from_pdf(pdf_path)

candidate_answers = """
1. Operational Oversight
"During peak seasons, I implement SOPs that prioritize speed without compromising service quality. For example, I introduce a color-coded task system for housekeeping and a fast-track check-in process for returning guests. I also cross-train staff to handle multiple roles. The biggest challenge is maintaining consistency under pressure, so I schedule daily briefings and real-time feedback loops to stay agile."
2. Guest Satisfaction
"At my previous hotel, a guest was upset about a room not being ready. I personally apologized, offered a complimentary drink at the bar, and expedited housekeeping. I also upgraded their room and followed up with a handwritten note. The guest later left a 5-star review and became a repeat customer."
3. Financial Management
"I start by analyzing historical data, occupancy trends, and departmental expenses. I set KPIs like RevPAR, GOP, and labor cost ratios. To ensure adherence, I implement monthly budget reviews with department heads and use forecasting tools to adjust for seasonality."
4. Event Planning Experience
"I would design a themed weekend event—like a 'Local Flavors Festival'—promoted via Instagram reels and influencer partnerships. I’d collaborate with local vendors, offer package deals, and track ROI through booking codes. My approach includes pre-event buzz, real-time engagement, and post-event feedback."
5. Health and Safety Compliance
"I use microlearning modules and gamified quizzes to keep training engaging. For hotel-specific compliance, I’d include scenario-based drills and regular audits. I also assign safety champions in each department to reinforce accountability."
6. Tool Improvement
"I’d redesign the hotel management software to include a shared dashboard with real-time task updates, voice notes for maintenance, and automated alerts for room readiness. This would reduce miscommunication and improve turnaround time."
7. Cost Control Measures
"I’d implement energy-saving initiatives like motion-sensor lighting and linen reuse programs. I’d also renegotiate vendor contracts and introduce portion control in F&B. To ensure buy-in, I’d involve staff in brainstorming sessions and reward cost-saving ideas."
8. Learning Approach
"I first identified upselling gaps through mystery audits. Then, I created a training module using role-play and real guest scenarios. I used leaderboards and incentives to motivate staff. Effectiveness was measured through a 30% increase in average check value over 3 months.""
"""
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
{job_description}

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

evaluation_response = client.chat.completions.create(
    model="synapt-dev-gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a technical evaluator."},
        {"role": "user", "content": evaluation_prompt}
    ],
    temperature=0.5,
    max_tokens=500
)

evaluation = evaluation_response.choices[0].message.content
print("Evaluation and Score:\n", evaluation)
