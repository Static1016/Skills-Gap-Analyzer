# Skill Gap Analyzer 

An end-to-end **AI/ML system** that analyzes a candidate’s resume, identifies skill gaps for a target role (ML Engineer), computes a job-fit score, and recommends a personalized learning path.

Built to simulate **real-world hiring intelligence systems** using NLP, Machine Learning, and API-based deployment.

-----------------------------------------------------------------

## Features

* Resume analysis (PDF & text)
* Skill extraction using **hybrid NLP**:

  * Rule-based matching
  * Sentence embeddings (SBERT)
* Skill gap detection (missing / weak / strong skills)
* Job fit scoring (0–100)
* Personalized learning recommendations
* Production-style **FastAPI backend**
* Clean modular project structure

-----------------------------------------------------------------

## Problem Statement

Students and early professionals often struggle to understand:

* How well their current skills match a target role
* What skills they are missing
* What to learn next in a structured way

This project solves that by **automating resume evaluation and guidance** using Machine Learning.

-----------------------------------------------------------------

## System Architecture (High Level)

```
Resume (PDF/Text)
        ↓
Text Preprocessing (spaCy)
        ↓
Skill Extraction
  ├─ Rule-based (skills taxonomy)
  └─ Embedding-based (SBERT)
        ↓
Skill Scoring & Normalization
        ↓
Skill Gap Detection
        ↓
Job Fit Scoring
        ↓
Learning Recommendation Engine
        ↓
FastAPI REST API
```

-----------------------------------------------------------------

## ML & NLP Techniques Used

### Natural Language Processing

* Text cleaning & lemmatization (spaCy)
* Sentence embeddings using **Sentence Transformers (SBERT)**

### Machine Learning Concepts

* Feature engineering (skill vectors)
* Similarity scoring (cosine similarity)
* Explainable rule + ML hybrid approach

### Recommendation System

* Content-based recommendations
* Skill → learning resource mapping

---

## Tech Stack

* **Language:** Python 3.11
* **NLP:** spaCy, Sentence Transformers
* **ML:** scikit-learn, NumPy
* **Backend:** FastAPI
* **PDF Parsing:** PyMuPDF
* **API Docs:** Swagger (auto-generated)
* **Version Control:** Git

---

## Project Structure

```
skill-gap-analyzer/
│
├── api/                    # FastAPI entry point
│   └── main.py
│
├── src/
│   ├── preprocessing/      # Text & PDF processing
│   ├── extraction/         # Skill extraction logic
│   ├── scoring/            # Gap detection & fit scoring
│   └── recommendation/     # Learning recommendations
│
├── data/
│   ├── raw/                # Sample resumes & JDs
│   └── skills/             # Skill taxonomy & resources
│
├── tests/                  # Test scripts
├── requirements.txt
└── README.md
```

-----------------------------------------------------------------

## How to Run Locally

### 1. Clone repository

```bash
git clone <repo-url>
cd skill-gap-analyzer
```

### 2. Setup environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Start API

```bash
uvicorn api.main:app --reload
```

### 4. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

-----------------------------------------------------------------

## API Endpoints

### `POST /analyze-text`

Analyze raw resume text.

### `POST /analyze-resume`

Upload and analyze a **PDF resume**.

**Returns:**

* Job fit score
* Extracted skills with confidence
* Skill gaps
* Learning recommendations

-----------------------------------------------------------------

## Example Output

```json
{
  "job_fit_score": 62.4,
  "gaps": {
    "missing": ["docker", "model deployment"],
    "weak": ["pandas"],
    "strong": ["python", "scikit-learn"]
  },
  "recommendations": [
    {
      "skill": "docker",
      "resources": ["Docker fundamentals", "Docker for ML models"]
    }
  ]
}
```

-----------------------------------------------------------------

## Use Cases

* Students preparing for ML/AI roles
* Resume screening tools
* EdTech platforms
* Career guidance systems

-----------------------------------------------------------------

## Future Improvements

* Multiple target roles (Data Scientist, Backend, etc.)
* Proficiency prediction using supervised ML
* User dashboard & progress tracking
* Cloud deployment (Docker + AWS)
* ATS-style resume parsing improvements

-----------------------------------------------------------------

## Author

**Static**
Aspiring ML Engineer
Focused on applied AI, NLP, and production-ready ML systems

-----------------------------------------------------------------





