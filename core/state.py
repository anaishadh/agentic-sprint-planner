from typing import List, Optional
from pydantic import BaseModel, Field


class TeamMember(BaseModel):
    name: str
    skills: List[str]
    experience_level: str  # junior / mid / senior
    availability_hours_per_day: int


class Task(BaseModel):
    id: str
    description: str
    required_skills: List[str]
    estimated_hours: int
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending / in_progress / completed


class SprintState(BaseModel):
    # Inputs
    client_problem_statement: str
    sprint_length_days: int
    deadline: Optional[str] = None
    team: List[TeamMember]

    # Intermediate outputs
    research_notes: Optional[str] = None
    tasks: List[Task] = Field(default_factory=list)

    # Final outputs
    sprint_plan: Optional[str] = None
