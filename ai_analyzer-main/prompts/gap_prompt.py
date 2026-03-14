GAP_PROMPT = """
You are a career AI mentor.

User skills:
{user_skills}

Target role skills:
{role_skills}

Identify the missing skills.

Return ONLY valid JSON:

{{
 "missing_skills": [],
 "matching_skills": []
}}
"""