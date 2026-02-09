from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.job_parser import extract_job_description
from src.extraction.skill_extractor import extract_skills
from src.scoring.job_matcher import match_resume_to_job
from src.recommendation.recommender import recommend_learning
from src.utils.skill_loader import load_skills
from src.utils.pdf_reader import extract_text_from_pdf

# -----------------------
# APP INIT
# -----------------------
app = FastAPI(title="Skill Gap Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# LOAD RESOURCES (ONCE)
# -----------------------
SKILLS_PATH = "data/skills/skills.json"
RESOURCES_PATH = "data/skills/learning_resources.json"
ROLES_PATH = "data/roles/job_roles.json"

skills_dict = load_skills(SKILLS_PATH)
resources_dict = load_skills(RESOURCES_PATH)
roles_dict = load_skills(ROLES_PATH)

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/job-roles")
def get_job_roles():
    """
    Returns job categories and roles for frontend dropdowns.
    """
    return roles_dict

# -----------------------
# MAIN ANALYSIS ENDPOINT
# -----------------------
@app.post("/analyze-job")
async def analyze_job(
    category: str,
    role: str,
    job_input: str,
    file: UploadFile = File(...)
):
    """
    Unified analysis:
    Role + Job Description + Resume
    """

    # -------- Resume ----------
    resume_bytes = await file.read()
    resume_text = extract_text_from_pdf(resume_bytes)
    resume_clean = clean_text(resume_text)

    # -------- Job Description ----------
    job_text = extract_job_description(job_input)
    job_clean = clean_text(job_text)

    # -------- Skill Extraction ----------
    resume_skills = extract_skills(resume_clean, skills_dict)
    job_skills = extract_skills(job_clean, skills_dict)

    # -------- Role Fallback ----------
    role_entry = roles_dict.get(category, {}).get(role, {})

    # roles.json now has structure: { label, skills }
    role_skills = role_entry.get("skills", {})

    role_skills = {
    k.lower(): float(v)
    for k, v in role_skills.items()
    if isinstance(v, (int, float))
    }


    # If JD extraction failed, fall back to role template
    if not job_skills:
        job_skills = {
            skill: float(weight)
            for skill, weight in role_skills.items()
        }


    # -------- Matching ----------
    result = match_resume_to_job(resume_skills, job_skills)

    # -------- Recommendations ----------
    recommendations = recommend_learning(
        {"missing": result.get("missing_skills", [])},
        resources_dict
    )

    # -------- Final Response ----------
    return {
        "job_fit_score": result.get("job_fit_score", 0),
        "role": role,
        "gaps": {
            "missing": result.get("missing_skills", []),
            "weak": [],
            "strong": []
        },
        "skill_alignment": result.get("skill_alignment", {}),
        "recommendations": recommendations
    }
