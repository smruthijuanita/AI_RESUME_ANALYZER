def normalize(skill):

    skill = skill.lower().strip()

    mapping = {
        "ml": "machine learning",
        "ai": "artificial intelligence",
        "genai": "generative ai",
        "vector db": "vector databases",
        "rag": "rag"
    }

    if skill in mapping:
        return mapping[skill]

    return skill


def analyze_gap(llm, user_skills, role_skills):

    user_skills = [normalize(s) for s in user_skills]
    role_skills = [normalize(s) for s in role_skills]

    matching = []
    missing = []

    for skill in role_skills:

        if skill in user_skills:
            matching.append(skill)
        else:
            missing.append(skill)

    return {
        "missing_skills": missing,
        "matching_skills": matching
    }