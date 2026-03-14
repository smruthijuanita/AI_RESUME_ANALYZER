RESUME_SKILL_PROMPT = """
You are an expert AI resume parser.

Extract ALL technical skills mentioned in the resume.

Include:
- programming languages
- ML/DL frameworks
- tools
- databases
- AI technologies
- cloud technologies
- backend technologies

Return ONLY valid JSON:

{{
 "skills": [],
 "tools": [],
 "frameworks": [],
 "domains": []
}}

Rules:
- Do not include explanations
- Do not include text outside JSON
- Only extract skills explicitly mentioned

Resume:
{resume}
"""