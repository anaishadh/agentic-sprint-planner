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

print("\n=== RESEARCH NOTES ===")
print(final_state.research_notes)

print("\n=== TASKS & ASSIGNMENTS ===")
for task in final_state.tasks:
    print(f"""
{task.id}
Description      : {task.description}
Required Skills  : {', '.join(task.required_skills)}
Estimated Hours  : {task.estimated_hours}
Assigned To      : {task.assigned_to or 'Unassigned'}
""")

print("\n=== SPRINT SUMMARY ===")
print(final_state.sprint_plan)
print("\n=== DAILY DASHBOARD ===")
for member in initial_state.team:
    print(f"\n{member.name}'s schedule:")
    for task in final_state.tasks:
        if task.assigned_to == member.name and task.schedule:
            print(f"  {task.id} ({task.description}):")
            for s in task.schedule:
                print(f"    {s}")


