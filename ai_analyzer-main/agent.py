from utils.router import route_query
from utils.tools import job_tool, tutorial_tool, web_tool


SYSTEM_PROMPT = """You are an AI Career Guide.
You help users with career guidance, job suggestions, resume improvement,
skill development, interview preparation, and job search advice.

Rules:
- Always answer career-related questions.
- If resume is uploaded -> use resume context.
- If resume is NOT uploaded -> still answer normally.
- If resume is not uploaded, always add at the end:

\"Tip: Upload your resume so I can give more personalized career guidance.\"
"""

REMINDER = "Tip: Upload your resume so I can give more personalized career guidance."


def _build_prompt(question: str, resume_context: str, external_info: str) -> str:
    return f"""{SYSTEM_PROMPT}

Resume context:
{resume_context}

External info:
{external_info}

Question:
{question}
"""


def generate_career_response(pipeline, question: str, resume_uploaded: bool) -> str:
    route = route_query(question)

    resume_context = ""
    external_info = ""

    if resume_uploaded and pipeline.retriever:
        if route in {"resume", "hybrid"}:
            resume_context = pipeline._get_resume_context(question)
        if route in {"web", "hybrid"}:
            external_info = web_tool(question)
        elif route == "job":
            external_info = job_tool(question)
        elif route == "tutorial":
            external_info = tutorial_tool(question)
    else:
        if route == "job":
            external_info = job_tool(question)
        elif route == "tutorial":
            external_info = tutorial_tool(question)
        else:
            external_info = web_tool(question)

    prompt = _build_prompt(
        question=question,
        resume_context=resume_context,
        external_info=external_info,
    )
    answer = pipeline.llm.generate(prompt)

    if not resume_uploaded:
        answer = f"{answer}\n\n{REMINDER}"

    return answer
