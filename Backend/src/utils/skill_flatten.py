def extract_all_skills_from_roles(roles_dict):
    """
    Converts job_roles.json into a flat skill dictionary.
    """
    skills = {}

    for category in roles_dict.values():
        for role in category.values():
            for skill, weight in role["skills"].items():
                # keep max weight if skill appears multiple times
                skills[skill.lower()] = max(
                    skills.get(skill.lower(), 0.0),
                    float(weight)
                )

    return skills
