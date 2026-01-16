from core.state import SprintState, TeamMember
from graph.workflow import build_graph

graph = build_graph()

initial_state = SprintState(
    client_problem_statement="Design a user registration feature for a website",
    sprint_length_days=10,
    team=[
        TeamMember(
            name="Alice",
            skills=["frontend", "react"],
            experience_level="mid",
            availability_hours_per_day=6,
        ),
        TeamMember(
            name="Bob",
            skills=["backend", "python", "api"],
            experience_level="senior",
            availability_hours_per_day=6,
        ),
    ],
)

# Run graph
final_state_dict = graph.invoke(initial_state)

# Convert back to Pydantic object
final_state = SprintState(**final_state_dict)

print(final_state.research_notes)
for task in final_state.tasks:
    print(f"{task.id}: {task.description}")
