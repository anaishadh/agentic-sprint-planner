from core.state import SprintState


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

    Your task:
    - Identify what needs to be built
    - Highlight frontend, backend, and infrastructure concerns
    - Keep it concise and structured
    """

    # Temporary placeholder (we'll replace with LLM call on Day 3)
    state.research_notes = prompt.strip()
    return state
