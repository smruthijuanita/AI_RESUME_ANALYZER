ROADMAP_PROMPT = """
You are an AI career mentor.

Create a learning roadmap for the following missing skills:

{skills}

Return ONLY valid JSON in this format:

{{
 "roadmap":[
  {{
   "skill":"",
   "timeline":"",
   "projects":[],
   "resources":[]
  }}
 ]
}}
"""