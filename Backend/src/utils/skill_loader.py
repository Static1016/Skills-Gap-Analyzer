import json

def load_skills(path: str):
    with open(path, "r") as f:
        skills = json.load(f)

    # normalize keys
    return {k.lower(): v for k, v in skills.items()}
