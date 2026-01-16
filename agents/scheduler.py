from core.state import SprintState, Task, TeamMember
from typing import List
import math

print(">>> Running Sprint Scheduler Agent")

def schedule_tasks(state: SprintState) -> SprintState:
    """
    Distributes tasks assigned to team members across the sprint days
    according to each member's daily availability.
    """

    # Map member name -> availability hours per day
    availability = {m.name: m.availability_hours_per_day for m in state.team}

    # Track daily usage per member
    member_daily_hours = {m.name: [0]*state.sprint_length_days for m in state.team}

    for task in state.tasks:
        if not task.assigned_to:
            continue  # skip unassigned tasks

        member = task.assigned_to
        hours_remaining = task.estimated_hours
        task.schedule = []

        # Fill task across days
        for day in range(state.sprint_length_days):
            available_hours = availability[member] - member_daily_hours[member][day]
            if available_hours <= 0:
                continue

            hours_today = min(hours_remaining, available_hours)
            member_daily_hours[member][day] += hours_today
            hours_remaining -= hours_today
            task.schedule.append(f"Day {day+1}: {hours_today}h")

            if hours_remaining <= 0:
                break

        # If hours_remaining > 0, task spans more than sprint length
        if hours_remaining > 0:
            task.schedule.append(f"⚠️ {hours_remaining}h overflow")

    return state
