import os
from dotenv import load_dotenv
import openai
from core.state import SprintState

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def business_analyst_agent(state: SprintState) -> SprintState:
    """
    Acts as a Business Analyst.
    - Understands the client problem
    - Identifies high-level solution requirements
    """
    prompt = f"""
You are a senior business analyst.

Client problem:
{state.client_problem_statement}

Task:
- Identify what needs to be built
- Highlight frontend, backend, and infrastructure concerns
- Keep it concise and structured
"""

    # New OpenAI v1 interface
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    # Extract text
    state.research_notes = response.choices[0].message.content.strip()
    return state
