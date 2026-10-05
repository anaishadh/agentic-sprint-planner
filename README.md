# Agent-Assisted Sprint Planner

An agent-assisted sprint planning system that transforms a high-level client requirement into structured engineering tasks, assigns those tasks to team members based on skills and capacity, and produces a day-by-day sprint schedule.

The project explores a practical pattern for combining **LLM reasoning with deterministic business logic**: use an LLM where interpretation and decomposition are required, then use explicit algorithms for resource allocation and scheduling.

## What It Does

Given:

* A high-level client problem statement
* Sprint duration
* Team members
* Team member skills
* Team member experience levels
* Daily availability

The system:

1. Validates whether the client requirement is sufficiently clear to proceed.
2. Uses a **Business Analyst Agent** to interpret the requirement and identify technical considerations.
3. Uses a **Task Breakdown Agent** to convert the analysis into structured engineering tasks.
4. Validates generated tasks using **Pydantic** models.
5. Assigns tasks to team members based on required skills and available capacity.
6. Schedules assigned work across the sprint days while respecting daily availability.
7. Reports unassigned tasks and schedule overflow when the available capacity is insufficient.

## Architecture

```text
Client Problem
      │
      ▼
┌─────────────────────┐
│ Business Analyst    │
│ Agent               │
│                     │
│ Requirement →       │
│ structured analysis │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Task Breakdown      │
│ Agent               │
│                     │
│ Analysis → Tasks    │
│ + Estimates         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Task Allocator      │
│                     │
│ Skills + Capacity   │
│ → Task Assignment   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Sprint Scheduler    │
│                     │
│ Assignment + Daily  │
│ Availability →      │
│ Day-by-day schedule │
└──────────┬──────────┘
           │
           ▼
      Sprint Plan
```

The workflow is implemented using **LangGraph's `StateGraph`**, with a shared `SprintState` passed between each stage.

## Why a Stateful Workflow?

Sprint planning is inherently sequential:

* Requirements need to be understood before tasks can be created.
* Tasks need to exist before they can be assigned.
* Assignments need to exist before work can be scheduled.

Instead of passing loosely structured outputs between independent LLM calls, the system maintains a typed `SprintState` containing the problem statement, team information, research notes, tasks, and final planning information.

This makes the workflow easier to reason about and provides a single state object shared across the graph.

## Agent and Workflow Components

### 1. Business Analyst Agent

The Business Analyst Agent receives the original client problem statement and uses an LLM to identify what needs to be built and highlight relevant technical considerations.

It also performs an initial clarity check. Very short or missing problem statements cause the workflow to stop before downstream processing.

**Output:**

```text
SprintState.research_notes
```

The current implementation uses the OpenAI API with GPT-4 and a low temperature to produce structured, concise analysis.

---

### 2. Task Breakdown Agent

The Task Breakdown Agent converts the Business Analyst's research notes into engineering tasks.

The LLM is instructed to return only JSON containing:

* Task ID
* Description
* Required skills
* Estimated hours

The generated JSON is parsed and converted into Pydantic `Task` objects.

This creates a boundary between probabilistic LLM output and the structured state used by the rest of the application.

**Example task structure:**

```json
{
  "id": "TASK-1",
  "description": "Implement participant registration API",
  "required_skills": ["backend", "api"],
  "estimated_hours": 6
}
```

The agent currently requests between 4 and 8 tasks and requires realistic engineering estimates.

---

### 3. Task Allocator

Task allocation is handled deterministically rather than by another LLM.

For each task, the allocator:

* Finds team members with matching skills.
* Sorts eligible members by current assigned workload.
* Checks whether the task fits within their total sprint capacity.
* Assigns the task to the first eligible member who has sufficient capacity.
* Records tasks that cannot be assigned.

This separates **reasoning-heavy work** from **constraint-based work**.

The LLM determines what work is required; explicit application logic determines who can perform it.

---

### 4. Sprint Scheduler

The scheduler distributes each assigned task across the available sprint days.

For each team member, it tracks:

```text
daily available hours
daily hours already allocated
```

Tasks are then spread across the sprint until their estimated hours are exhausted.

If a task cannot fit within the sprint, the scheduler explicitly reports the remaining hours as overflow instead of silently dropping the work.

Example:

```text
Day 1: 6h
Day 2: 4h
⚠️ 2h overflow
```

## State Model

The workflow uses Pydantic models to maintain structured state.

### `TeamMember`

Contains:

* Name
* Skills
* Experience level
* Availability hours per day

### `Task`

Contains:

* ID
* Description
* Required skills
* Estimated hours
* Assigned team member
* Status
* Schedule

### `SprintState`

Contains:

* Client problem statement
* Sprint length
* Deadline
* Team
* Workflow continuation flag
* Business analysis
* Generated tasks
* Sprint summary

This provides a typed contract between the workflow stages.

## Technology Stack

* **Python**
* **LangGraph** — workflow orchestration and state transitions
* **Pydantic** — typed state and task validation
* **OpenAI API** — requirement analysis and task decomposition
* **LangChain** — project dependency / LLM application ecosystem
* **python-dotenv** — environment configuration

## Project Structure

```text
agentic-sprint-planner/
│
├── agents/
│   ├── business_analyst.py
│   ├── task_breakdown.py
│   ├── allocator.py
│   ├── scheduler.py
│   └── sprint_planner.py
│
├── core/
│   ├── config.py
│   └── state.py
│
├── graph/
│   └── workflow.py
│
├── docs/
│   ├── agent_roles.md
│   ├── problem_statement.md
│   ├── roadmap.md
│   └── system_design.md
│
├── outputs/
│   └── sample_sprint_plan.txt
│
├── run.py
└── requirements.txt
```

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/anaishadh/agentic-sprint-planner.git
cd agentic-sprint-planner
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the OpenAI API key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

### 5. Run

```bash
python run.py
```

The example workflow processes a sample technology-festival website requirement and prints:

* Business analysis
* Generated tasks
* Task assignments
* Sprint summary
* Daily schedules

## Design Principle: LLM Where Useful, Code Where Deterministic

A central design decision in this project is not to make every stage an autonomous LLM agent.

The system uses an LLM for tasks that require interpretation:

```text
Ambiguous requirement
        ↓
Business understanding
        ↓
Task decomposition
        ↓
Engineering estimates
```

Once the problem is represented structurally, deterministic Python logic handles:

```text
Skills
+
Capacity
+
Availability
        ↓
Task assignment
        ↓
Scheduling
```

This makes the system more predictable and easier to debug than an architecture where an LLM makes every planning decision.

## Current Limitations

The current implementation is intentionally an early-stage prototype.

Known limitations include:

* Task allocation currently matches a task when a team member has **any** of the task's required skills rather than requiring every skill.
* Allocation uses estimated hours and availability but does not yet account for task dependencies or priority.
* Scheduling is sequential and does not model task dependencies.
* The current workflow does not persist state between runs.
* The LLM-generated task estimates are not independently validated against historical engineering data.
* There is no automated evaluation framework for the quality of generated plans yet.
* The current workflow uses OpenAI directly rather than abstracting the model provider.
* The `Sprint Planner Agent` module is reserved for future development; the active workflow currently consists of the Business Analyst, Task Breakdown, Task Allocator, and Scheduler stages.
* Human approval checkpoints are part of the longer-term design direction but are not yet implemented in the current workflow.

## Roadmap

Potential next stages include:

### Phase 1 — Foundations

* Core state models
* Repository structure
* Initial agent implementations

### Phase 2 — Agent Orchestration

* Stateful LangGraph workflow
* Shared state between agents
* Conditional workflow execution

### Phase 3 — Planning Intelligence

* Task dependencies
* Task priorities
* More sophisticated resource allocation
* Better scheduling strategies

### Phase 4 — Human-in-the-Loop

* Review generated task breakdowns
* Allow users to modify or reject generated tasks
* Require approval before committing the final sprint plan

### Phase 5 — Evaluation

* Golden planning scenarios
* Automated evaluation of task quality
* Estimate accuracy
* Allocation quality
* Schedule feasibility

### Phase 6 — Productionization

* API layer
* Persistent state
* Authentication
* Observability
* Integration with project-management systems


