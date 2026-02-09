import json
from pathlib import Path
from collections import defaultdict

SKILLS_PATH = "data/skills/skills.json"

def load_skills():
    with open(SKILLS_PATH, "r") as f:
        return json.load(f)
    
def extract_skills_rule_based(tokens: list, skills_dict: dict) -> dict:
    #Returns frequency count of matched skills

    skill_freq = defaultdict(int)
    token_text = " ".join(tokens)

    for category, skills in skills_dict.items():
        for skill in skills:
            skill_clean = skill.lower()
            if skill_clean in token_text:
                skill_freq[skill_clean] += token_text.count(skill_clean)

    return dict(skill_freq)
