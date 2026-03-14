import json
import re
from prompts.roadmap_prompt import ROADMAP_PROMPT


def generate_roadmap(llm, missing_skills):

    prompt = ROADMAP_PROMPT.format(skills=missing_skills)

    response = llm.invoke(prompt)

    text = response.content

    try:
        roadmap = json.loads(text)

    except:

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            try:
                roadmap = json.loads(match.group())
            except:
                roadmap = {"roadmap": []}
        else:
            roadmap = {"roadmap": []}

    return roadmap