import os
import json
from dotenv import load_dotenv
import openai
from core.state import SprintState, Task

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def task_breakdown_agent(state: SprintState) -> SprintState:
    # In task_breakdown_agent / allocate_tasks / schedule_tasks
    if not state.can_proceed:
        print(">>> Skipping Task_breakdown agent because input is invalid")
        return state
    
    print(">>> Running Task Breakdown Agent")
    """
    Converts research notes into validated engineering tasks.
    Enforces strict JSON output.
    """

    system_prompt = """
You are a system that outputs ONLY valid JSON.
No explanations.
No markdown.
No extra text.
"""

    user_prompt = f"""
Based on the following research notes, generate a list of engineering tasks.

Research notes:
{state.research_notes}

Output MUST be valid JSON in the following format:

[
  {{
    "id": "TASK-1",
    "description": "Short task description",
    "required_skills": ["frontend", "backend"],
    "estimated_hours": 6
  }}
]

Rules:
- 4 to 8 tasks
- realistic engineering estimates
- skills must be relevant and categorize those skills under broader terms like frontend,backend,ML etc
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content.strip()

    # HARD FAIL if not JSON
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Task Breakdown Agent failed to return valid JSON.\nOutput was:\n{raw_output}"
        )

    # Validate with Pydantic
    state.tasks = [Task(**task) for task in parsed]
    return state
