from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import json

from src.extraction.skill_extractor import extract_skills
from src.scoring.job_matcher import match_resume_to_job
from src.recommendation.recommender import recommend_learning
from src.utils.pdf_reader import extract_text_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load job roles
with open("data/roles/job_roles.json") as f:
    JOB_ROLES = json.load(f)

# Simple learning resources
RESOURCES = {
    "api development": [
        {"title": "REST APIs with FastAPI", "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA"}
    ],
    "database design": [
        {"title": "Database Design Basics", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc"}
    ],
    "python": [
        {"title": "Python for Beginners", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"}
    ]
}


@app.post("/analyze-job")
async def analyze_job(
    category: str = Form(...),
    role: str = Form(...),
    resume: UploadFile = Form(...)
):
    # Extract resume text
    resume_text = extract_text_from_pdf(resume)

    # Load role skills
    role_data = JOB_ROLES[category][role]
    job_skills = {
        k.lower(): float(v)
        for k, v in role_data["skills"].items()
    }

    # Extract resume skills
    resume_skills = extract_skills(resume_text, job_skills.keys())

    # Match
    result = match_resume_to_job(resume_skills, job_skills)

    recommendations = recommend_learning(result, RESOURCES)

    return {
        "job_fit_score": result["fit_score"],
        "matched_skills": result["matched"],
        "gaps": {
            "missing": result["missing"],
            "weak": result["weak"]
        },
        "recommendations": recommendations,
        "role": role
    }

@app.get("/job-roles")
def get_job_roles():
    return JOB_ROLES
