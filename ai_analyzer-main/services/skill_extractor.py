import json
import re
from prompts.resume_prompt import RESUME_SKILL_PROMPT


def extract_skills(llm, resume_text):

    prompt = RESUME_SKILL_PROMPT.format(resume=resume_text)

    response = llm.invoke(prompt)

    text = response.content

    try:
        skills = json.loads(text)

    except:
        # Extract JSON block if model returns extra text
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            try:
                skills = json.loads(match.group())
            except:
                skills = {"skills": [], "tools": [], "frameworks": [], "domains": []}
        else:
            skills = {"skills": [], "tools": [], "frameworks": [], "domains": []}

    return skills