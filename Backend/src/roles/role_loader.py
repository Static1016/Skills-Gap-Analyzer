import json

ROLES_PATH = "data/roles/job_roles.json"

def load_roles():
    with open(ROLES_PATH, "r") as f:
        return json.load(f)

def get_role_skills(roles, category, role_key):
    return roles[category][role_key]["skills"]
