import os
from dotenv import load_dotenv
import openai
from core.state import SprintState, Task

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def task_breakdown_agent(state: SprintState) -> SprintState:
    """
    Converts research notes into structured engineering tasks.
    """
    prompt = f"""
You are a technical project manager.

Based on the following research notes, break the work into clear engineering tasks.

Research notes:
{state.research_notes}

Instructions:
- Return 4–8 tasks
- Each task should include:
  - Short description
  - Required skills
  - Estimated effort in hours
- Think like a real engineering team
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    raw_output = response.choices[0].message.content.strip()

    # Temporary naive parsing (we’ll improve later)
    tasks = []
    for idx, line in enumerate(raw_output.split("\n")):
        if line.strip():
            tasks.append(
                Task(
                    id=f"TASK-{idx+1}",
                    description=line.strip(),
                    required_skills=["backend"],  # placeholder
                    estimated_hours=4  # placeholder
                )
            )

    state.tasks = tasks
    return state
