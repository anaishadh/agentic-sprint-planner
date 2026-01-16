import os
from dotenv import load_dotenv
import openai
from core.state import SprintState

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

print(">>> Running Business Analyst Agent")

def business_analyst_agent(state: SprintState) -> SprintState:
    """
    Acts as a Business Analyst.
    - Understands the client problem
    - Identifies high-level solution requirements
    """

    # Early clarity check
    if not state.client_problem_statement or len(state.client_problem_statement.split()) < 5:
        state.sprint_plan = "❌ Client problem statement too vague or meaningless. Cannot proceed."
        state.can_proceed = False
        state.research_notes = None
        state.tasks = []  # clear tasks to prevent allocator from doing work
        return state


    prompt = f"""
You are a senior business analyst.

Client problem:
{state.client_problem_statement}

Task:
- Identify what needs to be built
- Highlight technical details (might include but not necessary: frontend, backend, and infrastructure concerns)
- Keep it concise and structured
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    state.research_notes = response.choices[0].message.content.strip()
    return state

