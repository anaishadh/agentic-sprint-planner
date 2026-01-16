from core.state import Task, TeamMember, SprintState
from typing import List

print(">>> Running Task Allocator Agent")

def allocate_tasks(state: SprintState) -> SprintState:
    """
    Assigns tasks to team members based on skills and availability.
    Updates task.assigned_to and member's used hours.
    """

    # Convert availability to total sprint hours
    member_capacity = {m.name: m.availability_hours_per_day * state.sprint_length_days for m in state.team}
    member_load = {m.name: 0 for m in state.team}  # hours assigned so far

    unassigned_tasks = []

    for task in state.tasks:
        # Eligible members: have all required skills
        eligible = [m for m in state.team if all(skill in m.skills for skill in task.required_skills)]

        # Sort eligible by least used hours (fair distribution)
        eligible.sort(key=lambda m: member_load[m.name])

        assigned = False
        for member in eligible:
            if member_load[member.name] + task.estimated_hours <= member_capacity[member.name]:
                task.assigned_to = member.name
                member_load[member.name] += task.estimated_hours
                assigned = True
                break

        if not assigned:
            unassigned_tasks.append(task)

    state.tasks = state.tasks  # update state
    state.sprint_plan = f"{len(unassigned_tasks)} tasks unassigned" if unassigned_tasks else "All tasks assigned"

    return state
