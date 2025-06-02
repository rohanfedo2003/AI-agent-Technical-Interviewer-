import pdfplumber
from openai import AzureOpenAI
client = AzureOpenAI(
    api_key="TYuzFHHVhPINPX5s6V7qMZ4xY7rEfEKgMryyj7TNh7t1w9fKdy1bJQQJ99BAACHYHv6XJ3w3AAABACOGkzZu",
    api_version="2024-05-01-preview",
    azure_endpoint="https://synapt-development-instance.openai.azure.com/"
)


def analyze_text_with_openai(text, job_description=None):
    prompt = f"""
**Resume Optimization Request with ATS Scoring**

As an ATS-optimization specialist, I will:
1. Calculate current ATS compatibility score (0-100)
2. Perform comprehensive improvements
3. Calculate optimized ATS score
4. Provide detailed change analysis
5. Output the optimized resume

=== ANALYSIS PROCESS ===
1. **Initial ATS Evaluation**:
   - Keyword density analysis
   - Section completeness check
   - Formatting compliance
   - Skills-to-requirements matching
   - Achievement quantification

2. **Optimization Phase**:
   - Grammar/spelling corrections
   - Structural improvements
   - {"Job-specific keyword optimization" if job_description else "General ATS enhancements"}
   - Achievement-oriented bullet points
   - Technical skill highlighting
   - Quantifiable results insertion

3. **Final Evaluation**:
   - Recalculate ATS score
   - Compare before/after results
   - Explain score changes

=== REQUIRED OUTPUT FORMAT ===
**INITIAL ATS SCORE**: [score]/100
- Key Strengths: [list 2-3]
- Critical Weaknesses: [list 2-3]

**OPTIMIZED ATS SCORE**: [score]/100 (+[change])
- Key Improvements: [list 3-5]
- Remaining Weaknesses: [list 1-2]

=== DETAILED CHANGES ===
For each modification:
- [CHANGE TYPE] Original: "[text]" → Improved: "[text]"
  Reason: [explanation of ATS impact]

=== FINAL RECOMMENDATIONS ===
[3-5 priority action items for further improvement]

=== OPTIMIZED RESUME ===
[Include the fully optimized resume here]

**Job Description**: {"Provided" if job_description else "Not provided"}
**Resume Content**:
{text}

**ATS Scoring Rubric**:
1. Keyword Optimization (25%)
2. Formatting & Structure (20%)
3. Quantifiable Achievements (20%) 
4. Skills/Experience Relevance (20%)
5. Professional Tone (15%)

Score Interpretation:
90-100: Excellent (Top 5%)
80-89: Strong (Top 20%)
70-79: Competitive (Top 40%)
60-69: Needs Improvement
<60: High Rejection Risk
"""

    response = client.chat.completions.create(
        model="synapt-dev-gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a certified professional resume writer with expertise in ATS optimization."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=3000,
        top_p=0.9
    )

    return response.choices[0].message.content


def extract_text_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as doc:
            for page in doc.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    return text.strip()

if __name__ == "__main__":
    pdf_path = input("Enter PDF path: ")
    pdf_text = extract_text_pdfplumber(pdf_path)
    result=analyze_text_with_openai(pdf_text)
    print(result)



